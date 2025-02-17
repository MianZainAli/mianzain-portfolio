document.addEventListener('DOMContentLoaded', () => {
    const projectCards = document.querySelectorAll('.project-card');
    const filterContainer = document.querySelector('.project-filters');

    // Clear existing buttons
    filterContainer.innerHTML = '';

    // Add the "All" button first
    const allButton = document.createElement('button');
    allButton.className = 'filter-btn active';
    allButton.setAttribute('data-filter', 'all');
    allButton.textContent = 'All';
    filterContainer.appendChild(allButton);

    const categories = new Set();
    projectCards.forEach(card => {
        const category = card.getAttribute('data-category').charAt(0).toUpperCase() + card.getAttribute('data-category').slice(1);
        categories.add(category);
    });
    categories.forEach(category => {
        const button = document.createElement('button');
        button.className = 'filter-btn';
        button.setAttribute('data-filter', category);
        button.textContent = category.charAt(0).toUpperCase() + category.slice(1);
        filterContainer.appendChild(button);
    });

    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const selectedCategory = btn.getAttribute('data-filter').toLowerCase();
            projectCards.forEach(card => {
                const cardCategory = card.getAttribute('data-category').toLowerCase();
                card.style.display = (selectedCategory === 'all' || cardCategory === selectedCategory) ? 'block' : 'none';
            });
        });
    });
});
