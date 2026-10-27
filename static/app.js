document.addEventListener('DOMContentLoaded', () => {

    lucide.createIcons();

    const searchInput = document.querySelector('#searchInput');
    const statusFilter = document.querySelector('#statusFilter');
    const rows = [...document.querySelectorAll('#contractRows tr')];
    const visibleCount = document.querySelector('#visibleCount');
    const emptyState = document.querySelector('#emptyState');

    const modal = document.querySelector('#contractModal');
    const addContract = document.querySelector('#addContract');
    const closeModalButton = document.querySelector('#closeModal');
    const cancelModal = document.querySelector('#cancelModal');

    const contractForm = document.querySelector('#contractForm');


    // ==========================================
    // SEARCH & FILTER
    // ==========================================

    function filterRows() {

        if (!searchInput || !statusFilter) {
            return;
        }

        const query = searchInput.value.toLowerCase().trim();
        const status = statusFilter.value;

        let count = 0;

        rows.forEach((row) => {

            const matchesQuery =
                (row.dataset.search || '').toLowerCase().includes(query);

            const matchesStatus =
                status === 'all' ||
                row.dataset.status === status;

            const visible = matchesQuery && matchesStatus;

            row.hidden = !visible;

            if (visible) {
                count += 1;
            }
        });

        if (visibleCount) {
            visibleCount.textContent = count;
        }

        if (emptyState) {
            emptyState.hidden = count !== 0;
        }
    }


    if (searchInput) {
        searchInput.addEventListener('input', filterRows);
    }

    if (statusFilter) {
        statusFilter.addEventListener('change', filterRows);
    }


    // ==========================================
    // MODAL
    // ==========================================

    function closeModal() {

        if (!modal) {
            return;
        }

        modal.hidden = true;
        document.body.classList.remove('modal-open');
    }


    if (addContract && modal) {

        addContract.addEventListener('click', () => {

            modal.hidden = false;

            document.body.classList.add('modal-open');

            const firstInput = modal.querySelector('input');

            if (firstInput) {
                firstInput.focus();
            }
        });
    }


    if (closeModalButton) {
        closeModalButton.addEventListener('click', closeModal);
    }


    if (cancelModal) {
        cancelModal.addEventListener('click', closeModal);
    }


    if (modal) {

        modal.addEventListener('click', (event) => {

            if (event.target === modal) {
                closeModal();
            }

        });
    }


    // ==========================================
    // ESCAPE
    // ==========================================

    document.addEventListener('keydown', (event) => {

        if (
            event.key === 'Escape' &&
            modal &&
            !modal.hidden
        ) {
            closeModal();
        }

    });


    // ==========================================
    // FORM VALIDATION
    // ==========================================

    if (contractForm) {
        contractForm.addEventListener('submit', () => {
            console.log('Form kontrak dikirim');
        });
    }

});