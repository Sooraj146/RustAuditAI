use serde::Serialize;
use std::env;
use std::fs;
use std::io::{self, Read};
use syn::visit::Visit;
use syn::{Expr, ItemFn, Local, Stmt};

#[derive(Serialize, Debug)]
struct AnalysisOutput {
    success: bool,
    error: Option<String>,
    file_path: Option<String>,
    functions: Vec<FunctionAstInfo>,
}

#[derive(Serialize, Debug, Default)]
struct FunctionAstInfo {
    name: String,
    visibility: String,
    is_unsafe: bool,
    is_async: bool,
    inputs: Vec<String>,
    output_type: String,
    line_start: usize,
    line_end: usize,
    clone_count: usize,
    unsafe_block_count: usize,
    allocation_count: usize, // Box::new, Vec::new, String::from, etc.
    loop_count: usize,
    branch_count: usize, // if, match, else
    borrow_count: usize, // & / &mut
    statements: Vec<StatementSummary>,
}

#[derive(Serialize, Debug)]
struct StatementSummary {
    kind: String,
    code: String,
    has_clone: bool,
    has_unsafe: bool,
    has_allocation: bool,
    line_number: usize,
}

struct FunctionVisitor {
    functions: Vec<FunctionAstInfo>,
}

impl<'ast> Visit<'ast> for FunctionVisitor {
    fn visit_item_fn(&mut self, node: &'ast ItemFn) {
        let fn_name = node.sig.ident.to_string();
        let node_vis = &node.vis;
        let vis = quote::quote!(#node_vis).to_string();
        let is_unsafe = node.sig.unsafety.is_some();
        let is_async = node.sig.asyncness.is_some();

        let inputs: Vec<String> = node
            .sig
            .inputs
            .iter()
            .map(|arg| quote::quote!(#arg).to_string())
            .collect();

        let sig_output = &node.sig.output;
        let output_type = quote::quote!(#sig_output).to_string();

        let mut info = FunctionAstInfo {
            name: fn_name,
            visibility: vis,
            is_unsafe,
            is_async,
            inputs,
            output_type,
            line_start: 0,
            line_end: 0,
            ..Default::default()
        };

        // Analyze function body
        analyze_fn_body(&node.block, &mut info);

        self.functions.push(info);

        // Continue visiting nested items if any
        syn::visit::visit_item_fn(self, node);
    }
}

fn analyze_fn_body(block: &syn::Block, info: &mut FunctionAstInfo) {
    for stmt in &block.stmts {
        let code = quote::quote!(#stmt).to_string();
        let mut stmt_info = StatementSummary {
            kind: get_stmt_kind(stmt),
            code,
            has_clone: false,
            has_unsafe: false,
            has_allocation: false,
            line_number: 0,
        };

        inspect_stmt(stmt, info, &mut stmt_info);
        info.statements.push(stmt_info);
    }
}

fn get_stmt_kind(stmt: &Stmt) -> String {
    match stmt {
        Stmt::Local(_) => "LocalLet".to_string(),
        Stmt::Item(_) => "Item".to_string(),
        Stmt::Expr(expr, None) => format!("Expr({})", get_expr_kind(expr)),
        Stmt::Expr(expr, Some(_)) => format!("SemiExpr({})", get_expr_kind(expr)),
        Stmt::Macro(_) => "Macro".to_string(),
    }
}

fn get_expr_kind(expr: &Expr) -> &'static str {
    match expr {
        Expr::Call(_) => "Call",
        Expr::MethodCall(_) => "MethodCall",
        Expr::If(_) => "If",
        Expr::Match(_) => "Match",
        Expr::Loop(_) | Expr::While(_) | Expr::ForLoop(_) => "Loop",
        Expr::Unsafe(_) => "UnsafeBlock",
        Expr::Binary(_) => "BinaryOp",
        Expr::Unary(_) => "UnaryOp",
        Expr::Reference(_) => "Reference",
        Expr::Path(_) => "Path",
        Expr::Assign(_) => "Assign",
        Expr::Block(_) => "Block",
        Expr::Closure(_) => "Closure",
        _ => "Other",
    }
}

struct ExprVisitor<'a> {
    info: &'a mut FunctionAstInfo,
    stmt_info: &'a mut StatementSummary,
}

impl<'a, 'ast> Visit<'ast> for ExprVisitor<'a> {
    fn visit_expr(&mut self, expr: &'ast Expr) {
        match expr {
            Expr::MethodCall(mc) => {
                let method_name = mc.method.to_string();
                if method_name == "clone" {
                    self.info.clone_count += 1;
                    self.stmt_info.has_clone = true;
                }
                if method_name == "to_vec" || method_name == "to_string" || method_name == "to_owned" {
                    self.info.allocation_count += 1;
                    self.stmt_info.has_allocation = true;
                }
            }
            Expr::Call(call) => {
                let func_code = quote::quote!(#call.func).to_string();
                if func_code.contains("Box :: new")
                    || func_code.contains("Vec :: new")
                    || func_code.contains("String :: from")
                    || func_code.contains("rc :: Rc :: new")
                    || func_code.contains("sync :: Arc :: new")
                {
                    self.info.allocation_count += 1;
                    self.stmt_info.has_allocation = true;
                }
            }
            Expr::Unsafe(_) => {
                self.info.unsafe_block_count += 1;
                self.stmt_info.has_unsafe = true;
            }
            Expr::If(_) | Expr::Match(_) => {
                self.info.branch_count += 1;
            }
            Expr::Loop(_) | Expr::While(_) | Expr::ForLoop(_) => {
                self.info.loop_count += 1;
            }
            Expr::Reference(_) => {
                self.info.borrow_count += 1;
            }
            _ => {}
        }
        syn::visit::visit_expr(self, expr);
    }
}

fn inspect_stmt(stmt: &Stmt, info: &mut FunctionAstInfo, stmt_info: &mut StatementSummary) {
    let mut visitor = ExprVisitor { info, stmt_info };
    match stmt {
        Stmt::Local(Local { init, .. }) => {
            if let Some(init) = init {
                visitor.visit_expr(&init.expr);
            }
        }
        Stmt::Expr(expr, _) => {
            visitor.visit_expr(expr);
        }
        _ => {}
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let (code, file_path) = if args.len() > 1 {
        let path = &args[1];
        match fs::read_to_string(path) {
            Ok(content) => (content, Some(path.clone())),
            Err(e) => {
                let output = AnalysisOutput {
                    success: false,
                    error: Some(format!("Failed to read file '{}': {}", path, e)),
                    file_path: Some(path.clone()),
                    functions: vec![],
                };
                println!("{}", serde_json::to_string_pretty(&output).unwrap());
                return;
            }
        }
    } else {
        let mut buffer = String::new();
        if let Err(e) = io::stdin().read_to_string(&mut buffer) {
            let output = AnalysisOutput {
                success: false,
                error: Some(format!("Failed to read from stdin: {}", e)),
                file_path: None,
                functions: vec![],
            };
            println!("{}", serde_json::to_string_pretty(&output).unwrap());
            return;
        }
        (buffer, None)
    };

    match syn::parse_file(&code) {
        Ok(syntax_tree) => {
            let mut visitor = FunctionVisitor { functions: vec![] };
            visitor.visit_file(&syntax_tree);

            let output = AnalysisOutput {
                success: true,
                error: None,
                file_path,
                functions: visitor.functions,
            };
            println!("{}", serde_json::to_string_pretty(&output).unwrap());
        }
        Err(e) => {
            let output = AnalysisOutput {
                success: false,
                error: Some(format!("Rust syntax parse error: {}", e)),
                file_path,
                functions: vec![],
            };
            println!("{}", serde_json::to_string_pretty(&output).unwrap());
        }
    }
}
