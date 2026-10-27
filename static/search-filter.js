document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("searchInput");
    const statusFilter = document.getElementById("statusFilter");
    const tableBody = document.getElementById("contractTableBody");
    const visibleCount = document.getElementById("visibleCount");

    let contractData = [];
    let searchTimeout;

    async function loadContracts() {

        const search = searchInput.value.trim();
        const status = statusFilter.value;

        const params = new URLSearchParams({
            search: search,
            status: status
        });

        try {

            const response = await fetch(
                `/api/kontrak?${params.toString()}`
            );

            if (!response.ok) {
                throw new Error("Gagal mengambil data kontrak");
            }

            const result = await response.json();

            // SIMPAN data setelah fetch berhasil
            contractData = result.data;

            // Render tabel
            renderContracts(result.data);

            // Update jumlah kontrak
            visibleCount.textContent = result.total;

        } catch (error) {

            console.error("Error:", error);

        }
    }

    function renderContracts(data) {

        tableBody.innerHTML = "";

        if (data.length === 0) {

            tableBody.innerHTML = `
            <tr>
                <td colspan="7"
                    class="py-10 text-center text-slate-400">
                    Tidak ada kontrak ditemukan.
                </td>
            </tr>
        `;

            if (visibleCount) {
                visibleCount.textContent = "0";
            }

            return;
        }

        if (visibleCount) {
            visibleCount.textContent = data.length;
        }

        data.forEach(kontrak => {

            const row = document.createElement("tr");

            row.className = "align-top";

            row.innerHTML = `

            <!-- KONTRAK -->
            <td class="py-4 pr-4">

                <p class="text-xs font-semibold text-brand-700">
                    KZ1-026-${String(kontrak.id).padStart(3, "0")}
                </p>

                <p class="font-semibold text-slate-800">
                    ${kontrak.judul ?? "-"}
                </p>

                <p class="text-xs text-slate-400 mt-0.5">
                    Anggaran
                    ${formatRupiah(kontrak.anggaran)}
                </p>

            </td>


            <!-- LOKASI -->
            <td class="py-4 pr-4 text-slate-500">

                <span class="flex items-center gap-1.5">

                    <i data-lucide="map-pin"
                       class="w-3.5 h-3.5 shrink-0"></i>

                    ${kontrak.lokasi ?? "-"}

                </span>

            </td>


            <!-- WP&B / NILAI -->
            <td class="py-4 pr-4">

                <p class="text-xs text-slate-400">
                    WP&B ${kontrak.tahun_wpb ?? "-"}
                </p>

                <p class="font-semibold text-slate-800">
                    ${formatRupiah(kontrak.nilai)}
                </p>

            </td>


            <!-- TARGET -->
            <td class="py-4 pr-4 text-slate-500">

                <span class="flex items-center gap-1.5">

                    <i data-lucide="target"
                       class="w-3.5 h-3.5 shrink-0"></i>

                    ${formatTanggal(kontrak.target_realisasi)}

                </span>

            </td>


            <!-- PIC -->
            <td class="py-4 pr-4 text-slate-500">

                <span class="flex items-center gap-1.5">

                    <i data-lucide="user"
                       class="w-3.5 h-3.5 shrink-0"></i>

                    ${kontrak.pic ?? "-"}

                </span>

            </td>


            <!-- STATUS + PROGRESS -->
            <td class="py-4 pr-4 min-w-[160px]">

                <span
                    data-contract-status="${kontrak.id}"
                    class="inline-block text-[11px] font-semibold
                           px-2.5 py-1 rounded-full mb-1.5
                           ${getStatusClass(kontrak.status)}">

                    ${kontrak.status ?? "-"}

                </span>

                <div class="flex items-center gap-2">

                    <div class="h-1.5 flex-1 rounded-full
                                bg-slate-100 overflow-hidden">

                        <div
                            class="h-full rounded-full bg-sky-500"
                            style="width: ${kontrak.progress ?? 0}%">
                        </div>

                    </div>

                    <span class="text-xs font-semibold text-slate-600">
                        ${kontrak.progress ?? 0}%
                    </span>

                </div>

            </td>


            <!-- DETAIL -->
           
        `;

            tableBody.appendChild(row);

        });

        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }
    }

    function getStatusClass(status) {
        switch (status) {
            case "Persiapan Dokumen":
                return "bg-slate-100 text-slate-700";

            case "Routing & Persetujuan":
                return "bg-amber-100 text-amber-700";

            case "Submit SmartGEP":
                return "bg-blue-100 text-blue-700";

            case "Siap Proses Tender":
                return "bg-green-100 text-green-700";

            default:
                return "bg-slate-100 text-slate-700";
        }
    }

    function showToast(type, message) {

        const toast = document.getElementById("toast");
        const icon = document.getElementById("toastIcon");
        const title = document.getElementById("toastTitle");
        const text = document.getElementById("toastMessage");

        // Reset class
        toast.className = `
        fixed top-5 right-5 z-[9999]
        min-w-[320px] max-w-sm
        rounded-xl border bg-white
        shadow-lg px-4 py-3
        transition-all duration-300
    `;

        icon.className = `
        flex h-9 w-9 shrink-0 items-center justify-center rounded-full
    `;

        if (type === "success") {

            toast.classList.add("border-green-200");

            icon.classList.add(
                "bg-green-100",
                "text-green-600"
            );

            icon.innerHTML = `
            <i data-lucide="check-circle" class="w-5 h-5"></i>
        `;

            title.textContent = "Berhasil";

        } else {

            toast.classList.add("border-red-200");

            icon.classList.add(
                "bg-red-100",
                "text-red-600"
            );

            icon.innerHTML = `
            <i data-lucide="circle-alert" class="w-5 h-5"></i>
        `;

            title.textContent = "Gagal";
        }

        text.textContent = message;

        toast.classList.remove("hidden");

        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }

        // Hilang otomatis setelah 3 detik
        clearTimeout(window.toastTimeout);

        window.toastTimeout = setTimeout(() => {
            hideToast();
        }, 3000);
    }


    function hideToast() {

        const toast = document.getElementById("toast");

        toast.classList.add("hidden");
    }

    function formatRupiah(value) {

        if (
            value === null ||
            value === undefined ||
            value === ""
        ) {
            return "-";
        }

        return new Intl.NumberFormat("id-ID", {
            style: "currency",
            currency: "IDR",
            maximumFractionDigits: 0
        }).format(Number(value));

    }


    function formatTanggal(tanggal) {
        if (!tanggal) return "-";

        const date = new Date(tanggal);

        return date.toLocaleDateString("id-ID", {
            day: "2-digit",
            month: "short",
            year: "numeric"
        });
    }

    document.addEventListener("click", function (e) {

        const button = e.target.closest(".btn-edit");

        if (!button) return;

        const id = Number(button.dataset.id);

        const kontrak = contractData.find(
            item => item.id === id
        );

        if (!kontrak) {
            alert("Data kontrak tidak ditemukan.");
            return;
        }

        document.getElementById("editId").value =
            kontrak.id;

        document.getElementById("editJudul").value =
            kontrak.judul ?? "";

        document.getElementById("editLokasi").value =
            kontrak.lokasi ?? "";

        // const editPic = document.getElementById("editPic");

        // editPic.value = String(kontrak.pic ?? "");

        // console.log("PIC dari database:", kontrak.pic);
        // console.log("PIC yang dipilih:", editPic.value);

        document.getElementById("editAnggaran").value =
            kontrak.anggaran ?? "";

        document.getElementById("editNilai").value =
            kontrak.nilai ?? "";

        document.getElementById("editTahunWpb").value =
            kontrak.tahun_wpb ?? "";

        document.getElementById("editStatus").value =
            kontrak.status ?? "";

        document.getElementById("editTargetRealisasi").value =
            kontrak.target_realisasi ?? "";

        console.log("Target:", kontrak.target_realisasi);

        document.getElementById("editModal")
            .classList.remove("hidden");

    });

    document.getElementById("closeEditModal")
        .addEventListener("click", function () {

            document.getElementById("editModal")
                .classList.add("hidden");

        });


    document.getElementById("cancelEdit")
        .addEventListener("click", function () {

            document.getElementById("editModal")
                .classList.add("hidden");

        });

    // document.addEventListener("click", function (e) {

    //     const button = e.target.closest(".btn-delete");

    //     if (!button) return;

    //     const id = button.dataset.id;

    //     const yakin = confirm(
    //         "Apakah Anda yakin ingin menghapus kontrak ini?"
    //     );

    //     if (!yakin) return;

    //     fetch(`/api/kontrak/${id}`, {
    //         method: "DELETE"
    //     })
    //         .then(response => response.json())
    //         .then(result => {

    //             if (!result.success) {
    //                 alert(result.message);
    //                 return;
    //             }

    //             alert(result.message);

    //             // Muat ulang data tabel melalui AJAX
    //             loadContracts();

    //         })
    //         .catch(error => {
    //             console.error(error);
    //             alert("Terjadi kesalahan saat menghapus kontrak.");
    //         });
    // });

    let deleteContractId = null;

    document.addEventListener("click", function (e) {

        const button = e.target.closest(".btn-delete");

        if (!button) return;

        deleteContractId = button.dataset.id;

        showDeleteModal();
    });


    function showDeleteModal() {

        const modal = document.getElementById("deleteModal");

        modal.classList.remove("hidden");
        modal.classList.add("flex");

        if (typeof lucide !== "undefined") {
            lucide.createIcons();
        }
    }


    function hideDeleteModal() {

        deleteContractId = null;

        const modal = document.getElementById("deleteModal");

        modal.classList.add("hidden");
        modal.classList.remove("flex");
    }


    // Tombol Batal
    document.getElementById("cancelDelete").addEventListener("click", function () {
        hideDeleteModal();
    });


    // Tombol Hapus
    document.getElementById("confirmDelete").addEventListener("click", async function () {

        if (!deleteContractId) return;

        const id = deleteContractId;
        const button = this;

        button.disabled = true;
        button.textContent = "Menghapus...";

        try {

            const response = await fetch(`/api/kontrak/${id}`, {
                method: "DELETE"
            });

            const result = await response.json();

            if (!response.ok || !result.success) {

                showToast(
                    "error",
                    result.message || "Gagal menghapus kontrak"
                );

                return;
            }

            // Tutup modal
            hideDeleteModal();

            // Tampilkan toast
            showToast(
                "success",
                result.message || "Kontrak berhasil dihapus"
            );

            // Refresh tabel melalui AJAX
            loadContracts();

        } catch (error) {

            console.error(error);

            showToast(
                "error",
                "Terjadi kesalahan saat menghapus kontrak."
            );

        } finally {

            button.disabled = false;
            button.textContent = "Hapus";
        }

    });

    searchInput.addEventListener("input", function () {

        clearTimeout(searchTimeout);

        searchTimeout = setTimeout(() => {

            loadContracts();

        }, 300);

    });

    statusFilter.addEventListener("change", function () {

        loadContracts();

    });


    document.getElementById("editContractForm").addEventListener("submit", async function (e) {

        e.preventDefault();

        const id = document.getElementById("editId").value;

        const data = {
            judul_kontrak: document.getElementById("editJudul").value,
            lokasi_kontrak: document.getElementById("editLokasi").value,
            // pic: document.getElementById("editPic").value,
            anggaran: document.getElementById("editAnggaran").value,
            nilai: document.getElementById("editNilai").value,
            tahun_wpb: document.getElementById("editTahunWpb").value,
            status: document.getElementById("editStatus").value,
            target_realisasi: document.getElementById("editTargetRealisasi").value
        };

        console.log("UPDATE ID:", id);
        console.log("UPDATE DATA:", data);

        try {

            const response = await fetch(`/api/kontrak/${id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            console.log("UPDATE RESPONSE:", result);

            if (!response.ok || !result.success) {

                showToast(
                    "error",
                    result.message || "Gagal memperbarui kontrak"
                );

                return;
            }

            showToast(
                "success",
                "Kontrak berhasil diperbarui"
            );

            // Tutup modal
            document.getElementById("editModal")
                .classList.add("hidden");

            // Refresh tabel tanpa reload halaman
            loadContracts();

        } catch (error) {

            console.error("Error update kontrak:", error);

            alert("Terjadi kesalahan saat memperbarui kontrak.");
        }

    });


    loadContracts();

});

