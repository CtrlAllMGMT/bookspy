document.addEventListener('DOMContentLoaded', function() {
    const tables = document.querySelectorAll('.table');

    tables.forEach(table => {
        table.addEventListener('mouseover', function(event) {
            if (event.target.tagName === 'TR') {
                event.target.classList.add('table-hover');
            }
        });

        table.addEventListener('mouseout', function(event) {
            if (event.target.tagName === 'TR') {
                event.target.classList.remove('table-hover');
            }
        });
    });
});