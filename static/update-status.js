const overlay = document.getElementById('modal-overlay');
const closeModalBtn = document.getElementById('close-modal-btn');
const closeFooterModalBtn = document.getElementById('close-modal-footer-btn');

const openModalButtons = document.querySelectorAll('.open-modal-btn');

openModalButtons.forEach(button => {
    button.addEventListener('click', () => {

        const id = button.dataset.id;
        const judul = button.dataset.judul;
        const lokasi = button.dataset.lokasi;
        const anggaran = button.dataset.anggaran;
        const nilai = button.dataset.nilai;
        const wpb = button.dataset.wpb;
        const target = button.dataset.target;
        const pic = button.dataset.pic;
        const status = button.dataset.status;
        const progress = button.dataset.progress;

        // Isi modal
        document.getElementById('modal-contract-code').textContent =
            `KZ1-026-${String(id).padStart(3, '0')}`;

        document.getElementById('modal-contract-title').textContent =
            judul;

        document.getElementById('modal-lokasi').textContent =
            lokasi;

        document.getElementById('modal-pic').textContent =
            pic;

        document.getElementById('modal-anggaran').textContent =
            formatRupiah(anggaran);

        document.getElementById('modal-nilai').textContent =
            formatRupiah(nilai);

        document.getElementById('modal-wpb').textContent =
            wpb;

        document.getElementById('modal-target').textContent =
            target;

        document.getElementById('modal-status').value =
            status;

        document.getElementById('modal-progress-bar').style.width =
            `${progress}%`;

        document.getElementById('modal-progress').textContent =
            `${progress}%`;

        // Simpan ID kontrak yang sedang dibuka
        overlay.dataset.contractId = id;

        // Buka modal
        overlay.classList.remove('hidden');
    });
});

if (closeModalBtn && overlay) {
    closeModalBtn.addEventListener('click', () => {
        overlay.classList.add('hidden');
    });
}

if (closeFooterModalBtn && overlay) {
    closeFooterModalBtn.addEventListener('click', () => {
        overlay.classList.add('hidden');
    });
}

if (overlay) {
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.classList.add('hidden');
        }
    });
}

function formatRupiah(value) {
    return 'Rp ' + Number(value || 0).toLocaleString('id-ID');
}

const statusSelect = document.getElementById('modal-status');

if (statusSelect && overlay) {

    statusSelect.addEventListener('change', async function () {

        const kontrakId = overlay.dataset.contractId;
        const statusBaru = this.value;

        try {

            const response = await fetch(
                `/update-status/${kontrakId}`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        status: statusBaru
                    })
                }
            );

            const result = await response.json();

            if (!result.success) {
                alert(result.message);
                return;
            }

            const statusElement = document.querySelector(
                `[data-contract-status="${kontrakId}"]`
            );

            if (statusElement) {

                let badgeClass = '';

                if (statusBaru === 'Aktif') {
                    badgeClass = 'bg-green-50 text-green-700';
                }
                else if (statusBaru === 'Menunggu perpanjangan') {
                    badgeClass = 'bg-amber-50 text-amber-700';
                }
                else if (statusBaru === 'Draft') {
                    badgeClass = 'bg-slate-100 text-slate-600';
                }

                statusElement.innerHTML = `
                    <span class="${badgeClass} px-2.5 py-1 rounded-full">
                        ${statusBaru}
                    </span>
                `;
            }

            console.log('Status berhasil diperbarui');

        } catch (error) {

            console.error(error);
            alert('Gagal menyimpan perubahan status.');

        }
    });
}