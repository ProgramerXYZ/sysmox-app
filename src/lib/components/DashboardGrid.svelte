<script>
	const stats = [
		{
			title: 'CPU',
			value: '0%',
			id: 'cpu-chart'
		},
		{
			title: 'RAM',
			value: '0%',
			id: 'ram-chart'
		},
		{
			title: 'GPU',
			value: '0%',
			id: 'gpu-chart'
		},
		{
			title: 'Network',
			value: '0 KB/s',
			id: 'network-chart'
		}
	];
</script>

<section id="dashboard-grid">
	{#each stats as stat}
		<div class="stat-card">
			<div class="card-header">
				<h2>{stat.title}</h2>
				<span>{stat.value}</span>
			</div>

			<div class="chart-container" id={stat.id}></div>
		</div>
	{/each}
</section>