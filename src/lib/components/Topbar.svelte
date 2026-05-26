<script>
	export let systemStatus = 'System Running';

	let currentTime = '00:00:00';

	function updateClock() {
		currentTime = new Date().toLocaleTimeString();
	}

	updateClock();
	setInterval(updateClock, 1000);
</script>

<header id="topbar">
	<div id="system-status-container">
		<div class="status-dot"></div>

		<span id="system-status-text">
			{systemStatus}
		</span>
	</div>

	<div id="topbar-right-section">
		<div id="clock-container">
			<span id="clock-text">{currentTime}</span>
		</div>
	</div>
</header>