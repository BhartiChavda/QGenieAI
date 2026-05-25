document.addEventListener("DOMContentLoaded", function() {
    // Delete Confirmation handler
    const deleteButtons = document.querySelectorAll(".confirm-delete");
    deleteButtons.forEach(button => {
        button.addEventListener("click", function(e) {
            const itemName = this.getAttribute("data-item") || "this item";
            const confirmMsg = `Are you absolutely sure you want to delete ${itemName}? This action is permanent and cannot be undone!`;
            if (!confirm(confirmMsg)) {
                e.preventDefault();
            }
        });
    });

    // Real-time table search filter
    const searchInput = document.getElementById("adminSearch");

    if (searchInput) {
        searchInput.addEventListener("keyup", function() {
            const query = this.value.toLowerCase().trim();
            const tables = document.querySelectorAll("table.admin-table");
            
            tables.forEach(table => {
                const rows = table.querySelectorAll("tbody tr");
                rows.forEach(row => {
                    // Skip checking the empty placeholders
                    if (row.cells.length === 1 && row.cells[0].getAttribute("colspan")) {
                        return;
                    }
                    const textContent = row.textContent.toLowerCase();
                    if (textContent.includes(query)) {
                        row.style.display = "";
                    } else {
                        row.style.display = "none";
                    }
                });
            });
        });
    }
});
