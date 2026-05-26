<script>
	const processes = [
		{
			name: 'example.exe',
			cpu: '12%',
			ram: '250 MB',
			pid: 1234
		}
	];
</script>

<section id="process-section">
	<div class="section-title-container">
		<h2>Running Processes</h2>
	</div>

	<div id="process-table-container">
		<table id="process-table">
			<thead>
				<tr>
					<th>Process</th>
					<th>CPU</th>
					<th>RAM</th>
					<th>PID</th>
				</tr>
			</thead>

			<tbody>
				{#each processes as process}
					<tr>
						<td>{process.name}</td>
						<td>{process.cpu}</td>
						<td>{process.ram}</td>
						<td>{process.pid}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</section>