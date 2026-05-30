use tauri_plugin_shell::ShellExt;

#[tauri::command]
async fn start_backend(app: tauri::AppHandle) -> Result<(), String> {
    println!("Rust command called!");

    let command = app
        .shell()
        .sidecar("sysmoxBack")
        .map_err(|e| e.to_string())?;

    println!("Sidecar found!");

    let (_rx, _child) = command
        .spawn()
        .map_err(|e| e.to_string())?;

    println!("Sidecar spawned!");

    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            start_backend
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}