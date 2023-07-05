document.addEventListener('DOMContentLoaded', function () {
    // Number of items per page
    const itemsPerPage = 10;
    
    // The current page displayed
    let currentPage = 0;
    
    // Select all rows in the table
    const rows = Array.from(document.querySelectorAll('.table .row'));
    
    // Number of total pages
    const totalPages = Math.ceil(rows.length / itemsPerPage);
    
    function showPage(page) {
        // Hide all rows
        rows.forEach(row => row.style.display = 'none');
    
        // Calculate the start index
        const start = page * itemsPerPage;
    
        // Calculate the end index
        const end = start + itemsPerPage;
    
        // Show only the rows for this page
        rows.slice(start, end).forEach(row => row.style.display = '');
    }
    
    // Initially show the first page
    showPage(currentPage);
    
    // Add event listeners to all page buttons
    for (let i = 0; i < totalPages; i++) {
        const pageButton = document.querySelector(`.page-number[data-page="${i}"]`);
    
        if (pageButton) {
            pageButton.addEventListener('click', () => {
                currentPage = i;
                showPage(currentPage);
            });
        }
    }
});