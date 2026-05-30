<script>
	let collapsed = true;
	let animating = false;

	const navItems = [
		'Dashboard',
		'Processes',
		'Network',
		'Storage',
		'Settings'
	];

	function toggleSidebar() {
		animating = false;

		requestAnimationFrame(() => {
			requestAnimationFrame(() => {
				animating = true;
				collapsed = !collapsed;
			});
		});
	}

	function handleAnimationEnd() {
		animating = false;
	}
</script>

<aside
	id="sidebar"
	class:sidebar-collapsed={collapsed}
	class:sidebar-animating={animating}
	on:animationend={handleAnimationEnd}
>
	<div id="sidebar-top-section">
		<button id="sidebar-toggle-button" on:click={toggleSidebar}>
			{collapsed ? '›' : '☰'}
		</button>
	</div>

	<div id="logo-container">
		<h1 id="logo-text">SYSMOX</h1>
	</div>

	<nav id="sidebar-nav">
		{#each navItems as item}
			<button class="nav-button">
				{item}		
			</button>
		{/each}
	</nav>
</aside>