<script>
        import { invoke } from "@tauri-apps/api/core";

    async function startBackend() {
        try {
            await invoke("start_backend");
            console.log("Backend started!");
        } catch (err) {
            console.error(err);
        }
    }
</script>

<button onclick={startBackend} class="nav-button">
    Start Backend
</button>