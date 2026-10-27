document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.getElementById('logoutButton');
    const logoutModal = document.getElementById('logoutModal');
    const cancelLogout = document.getElementById('cancelLogout');

    if (!logoutButton || !logoutModal || !cancelLogout) return;

    // Tampilkan modal konfirmasi
    logoutButton.addEventListener('click', function () {
        logoutModal.classList.remove('hidden');
        logoutModal.classList.add('flex');
    });

    // Batalkan logout
    cancelLogout.addEventListener('click', function () {
        logoutModal.classList.add('hidden');
        logoutModal.classList.remove('flex');
    });

    // Tutup modal jika area luar diklik
    logoutModal.addEventListener('click', function (event) {
        if (event.target === logoutModal) {
            logoutModal.classList.add('hidden');
            logoutModal.classList.remove('flex');
        }
    });

    // Tutup modal dengan tombol Escape
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            logoutModal.classList.add('hidden');
            logoutModal.classList.remove('flex');
        }
    });
});