<script>
	import "../app.css";
	import Sidebar from '../lib/components/Sidebar.svelte';
	import Topbar from '../lib/components/Topbar.svelte';
	import DashboardGrid from '../lib/components/DashboardGrid.svelte';
	import SystemInfo from '../lib/components/SystemInfo.svelte';
	import ProcessTable from '../lib/components/ProcessTable.svelte';
	import BackendStartButton from "$lib/components/BackendStartButton.svelte";

	let systemStatus = 'System Running';
</script>

<svelte:head>
	<title>Sysmox</title>
</svelte:head>

<div id="app-container">
	<Sidebar />

	<main id="main-content">
		<Topbar {systemStatus} />
		<DashboardGrid />
		<SystemInfo />
		<ProcessTable />
		<BackendStartButton/>
	</main>
</div>