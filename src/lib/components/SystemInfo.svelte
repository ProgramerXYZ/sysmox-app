<script>
	const info = [
		{ label: 'OS', value: 'Unknown' },
		{ label: 'CPU', value: 'Unknown' },
		{ label: 'RAM', value: 'Unknown' },
		{ label: 'Temperature', value: '0°C' }
	];
</script>

<section id="system-details-section">
	<div id="system-info-card">
		<div class="section-title-container">
			<h2>System Information</h2>
		</div>

		<div id="system-info-grid">
			{#each info as item}
				<div class="info-box">
					<span class="info-label">{item.label}</span>
					<span class="info-value">{item.value}</span>
				</div>
			{/each}
		</div>
	</div>
</section>