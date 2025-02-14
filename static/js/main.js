async function fetchStats() {
    try {
      const response = await fetch('/api/stats');
      const stats = await response.json();
  
      document.getElementById('totalRequests').innerText = stats.total_requests;
      document.getElementById('successCount').innerText = stats.success_count;
      document.getElementById('errorCount').innerText = stats.error_count;
      document.getElementById('avgResponseTime').innerText =
        stats.average_response_time ? stats.average_response_time.toFixed(3) : "0";
  
      // Update the Most Commonly Accessed Endpoints table
      const endpointsTable = document.getElementById('commonEndpoints');
      endpointsTable.innerHTML = '';
      if (stats.common_endpoints && stats.common_endpoints.length > 0) {
        stats.common_endpoints.forEach(ep => {
          const row = document.createElement('tr');
          row.innerHTML = `<td>${ep.endpoint}</td><td>${ep.count}</td>`;
          endpointsTable.appendChild(row);
        });
      } else {
        endpointsTable.innerHTML = '<tr><td colspan="2">No endpoints recorded</td></tr>';
      }
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  }
  
  async function fetchLogs() {
    try {
      let url = '/api/logs';
      const statusFilter = document.getElementById('statusFilter').value;
      if (statusFilter) {
        url += `?status_code=${statusFilter}`;
      }
      const response = await fetch(url);
      const logs = await response.json();
      const tableBody = document.getElementById('logsTableBody');
      tableBody.innerHTML = '';
      logs.forEach(log => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${log.id}</td>
          <td>${log.timestamp}</td>
          <td>${log.method}</td>
          <td>${log.path}</td>
          <td>${log.request_body}</td>
          <td>${log.status_code}</td>
          <td>${log.response_time ? log.response_time.toFixed(3) : "N/A"}</td>
        `;
        tableBody.appendChild(row);
      });
    } catch (err) {
      console.error('Error fetching logs:', err);
    }
  }
  
  async function refreshData() {
    await Promise.all([fetchStats(), fetchLogs()]);
  }
  
  // Refresh stats and logs every 5 seconds
  setInterval(refreshData, 5000);
  window.onload = refreshData;
  