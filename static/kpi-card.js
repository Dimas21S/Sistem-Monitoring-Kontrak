document.addEventListener("DOMContentLoaded", function () {
    const kpi = document.getElementById("avgProgressKpi");
    const modal = document.getElementById("portfolioModal");
    const overlay = document.getElementById("portfolioOverlay");

    const closeButton = document.getElementById("closePortfolioModal");
    const closeFooter = document.getElementById("closePortfolioFooter");

    if (!kpi || !modal) return;

    function openModal() {
        modal.classList.remove("hidden");
        modal.classList.add("flex");
        document.body.classList.add("overflow-hidden");

        if (window.lucide) {
            window.lucide.createIcons();
        }

        closeButton?.focus();
    }

    function closeModal() {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.classList.remove("overflow-hidden");

        kpi.focus();
    }

    kpi.addEventListener("click", openModal);

    kpi.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            openModal();
        }
    });

    closeButton?.addEventListener("click", closeModal);
    closeFooter?.addEventListener("click", closeModal);
    overlay?.addEventListener("click", closeModal);

    document.addEventListener("keydown", function (event) {
        if (
            event.key === "Escape" &&
            !modal.classList.contains("hidden")
        ) {
            closeModal();
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const kpi = document.getElementById("attentionKpi");
    const modal = document.getElementById("attentionModal");
    const overlay = document.getElementById("attentionOverlay");

    const closeButton = document.getElementById("closeAttentionModal");
    const closeFooter = document.getElementById("closeAttentionFooter");

    if (!kpi || !modal) return;

    function openModal() {
        modal.classList.remove("hidden");
        modal.classList.add("flex");
        document.body.classList.add("overflow-hidden");

        if (window.lucide) {
            window.lucide.createIcons();
        }

        closeButton?.focus();
    }

    function closeModal() {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.classList.remove("overflow-hidden");
        kpi.focus();
    }

    kpi.addEventListener("click", openModal);

    kpi.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            openModal();
        }
    });

    closeButton?.addEventListener("click", closeModal);
    closeFooter?.addEventListener("click", closeModal);
    overlay?.addEventListener("click", closeModal);

    document.addEventListener("keydown", function (event) {
        if (
            event.key === "Escape" &&
            !modal.classList.contains("hidden")
        ) {
            closeModal();
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("allFollowUpModal");
    const openButton = document.getElementById("showAllFollowUp");
    const closeButton = document.getElementById("closeAllFollowUp");
    const closeFooterButton = document.getElementById(
        "closeAllFollowUpFooter"
    );

    if (!modal || !openButton) return;

    function openModal() {
        modal.classList.remove("hidden");
        modal.classList.add("flex");
        document.body.classList.add("overflow-hidden");

        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }

        closeButton?.focus();
    }

    function closeModal() {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.classList.remove("overflow-hidden");
        openButton.focus();
    }

    openButton.addEventListener("click", openModal);
    closeButton?.addEventListener("click", closeModal);
    closeFooterButton?.addEventListener("click", closeModal);

    // Tutup jika pengguna mengklik area gelap di luar modal
    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Tutup menggunakan tombol Escape
    document.addEventListener("keydown", function (event) {
        if (
            event.key === "Escape" &&
            !modal.classList.contains("hidden")
        ) {
            closeModal();
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const trigger = document.getElementById("totalBudgetKpi");
    const modal = document.getElementById("totalBudgetModal");
    const closeButton = document.getElementById("closeTotalBudgetModal");
    const closeFooter = document.getElementById(
        "closeTotalBudgetModalFooter"
    );

    if (!trigger || !modal) return;

    function openBudgetModal() {
        modal.classList.remove("hidden");
        modal.classList.add("flex");
        document.body.classList.add("overflow-hidden");

        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }

        closeButton?.focus();
    }

    function closeBudgetModal() {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.classList.remove("overflow-hidden");
        trigger.focus();
    }

    trigger.addEventListener("click", openBudgetModal);

    trigger.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            openBudgetModal();
        }
    });

    closeButton?.addEventListener("click", closeBudgetModal);
    closeFooter?.addEventListener("click", closeBudgetModal);

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeBudgetModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (
            event.key === "Escape" &&
            !modal.classList.contains("hidden")
        ) {
            closeBudgetModal();
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const trigger = document.getElementById("currentYearKpi");
    const modal = document.getElementById("currentYearModal");
    const closeButton = document.getElementById("closeCurrentYearModal");
    const closeFooter = document.getElementById(
        "closeCurrentYearModalFooter"
    );

    if (!trigger || !modal) return;

    function openModal() {
        modal.classList.remove("hidden");
        modal.classList.add("flex");
        document.body.classList.add("overflow-hidden");

        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }

        closeButton?.focus();
    }

    function closeModal() {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.classList.remove("overflow-hidden");
        trigger.focus();
    }

    trigger.addEventListener("click", openModal);

    trigger.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            openModal();
        }
    });

    closeButton?.addEventListener("click", closeModal);
    closeFooter?.addEventListener("click", closeModal);

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (
            event.key === "Escape" &&
            !modal.classList.contains("hidden")
        ) {
            closeModal();
        }
    });
});