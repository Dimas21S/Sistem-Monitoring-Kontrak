const kontrakSelect = document.getElementById("kontrak-select");
const completeBtn = document.getElementById("complete-btn");
const stageList = document.getElementById("stage-list");

const targetModal = document.getElementById("target-modal");
const btnTarget = document.getElementById("btn-target");
const btnCloseTarget = document.getElementById("btn-close-target");
const btnBatalTarget = document.getElementById("btn-batal-target");
const btnSimpanTarget = document.getElementById("btn-simpan-target");

const modalTargetHari = document.getElementById("modal-target-hari");
const modalTanggalMulai = document.getElementById("modal-tanggal-mulai");
const modalTanggalTarget = document.getElementById("modal-tanggal-target");
const modalTargetTitle = document.getElementById("modal-target-title");

// Modal target persyaratan
const itemTargetModal = document.getElementById("item-target-modal");
const btnCloseItemTarget = document.getElementById("btn-close-item-target");
const btnBatalItemTarget = document.getElementById("btn-batal-item-target");
const btnSimpanItemTarget = document.getElementById("btn-simpan-item-target");
const itemTargetHari = document.getElementById("item-target-hari");
const itemTanggalMulai = document.getElementById("item-tanggal-mulai");
const itemTanggalTarget = document.getElementById("item-tanggal-target");
const itemTargetModalTitle = document.getElementById("item-target-modal-title");

let activeChecklistItem = null;

kontrakData.forEach(data => {
    const option = document.createElement("option");
    option.value = data.kontrak.id;
    option.textContent = data.kontrak.judul_kontrak;
    kontrakSelect.appendChild(option);
});

let stages = [];
let activeIndex = 0;

function loadContractData(kontrakId) {
    const dataKontrak = kontrakData.find(
        item =>
            Number(item.kontrak.id) === Number(kontrakId)
    );

    if (!dataKontrak) {

        console.error(
            "Kontrak tidak ditemukan:",
            kontrakId
        );

        stages = [];

        if (stageList) {
            stageList.innerHTML = "";
        }
        return;
    }


    // Pastikan tahapan_data tersedia
    if (!Array.isArray(dataKontrak.tahapan_data)) {

        console.error(
            "tahapan_data bukan array:",
            dataKontrak.tahapan_data
        );
        stages = [];
        return;
    }

    stages = dataKontrak.tahapan_data.map(tahapan => {

        const checklistItems =
            Array.isArray(tahapan.checklist_items)
                ? tahapan.checklist_items
                : [];

        return {

            id_document: tahapan.dokumen.id,
            nomor_doc: tahapan.dokumen.nomor_thp,
            title: tahapan.dokumen.judul_dokumen,
            subtitle: tahapan.dokumen.subjudul || "",
            status: tahapan.status,

            items: checklistItems.map(item => ({
                id_checklist: item.id_checklist,
                id_item: item.id_item,
                nomor_item: item.nomor_item,
                label: item.label,
                tipe_item: item.tipe_item,
                is_required: item.is_required,
                is_done: Boolean(item.is_done),
                tanggal_mulai: item.tanggal_mulai,
                target_hari: item.target_hari,
                tanggal_target: item.tanggal_target,
                tanggal_selesai: item.tanggal_selesai
            }))
        };
    });

    stages.forEach((stage, index) => {

        console.log(
            `Tahap ${index + 1}: ${stage.title}`,
            stage.items
        );

    });

    activeIndex = 0;

    render();

}

if (kontrakSelect) {

    kontrakSelect.addEventListener(
        "change",
        function () {

            const kontrakId =
                parseInt(this.value);

            if (!kontrakId) {

                stages = [];
                activeIndex = 0;

                if (stageList) {
                    stageList.innerHTML = "";
                }
                return;
            }

            loadContractData(kontrakId);

        }
    );

} else {

    console.error(
        "❌ #kontrak-select tidak ditemukan"
    );

}

function renderSidebar() {

    const list =
        document.getElementById("stage-list");

    if (!list) {
        return;
    }


    list.innerHTML = "";


    stages.forEach((s, i) => {

        const doneCount =
            s.items.filter(
                item => item.is_done
            ).length;

        const total =
            s.items.length;

        const pct =
            total
                ? Math.round(
                    (doneCount / total) * 100
                )
                : 0;

        const isActive =
            i === activeIndex;

        const isComplete =
            total > 0 &&
            doneCount === total;


        const item =
            document.createElement("button");
        item.type = "button";

        item.className =
            `w-full text-left rounded-lg px-3 py-2.5 flex items-center gap-3 transition ${isActive
                ? "bg-teal-50 ring-1 ring-teal-200"
                : "hover:bg-slate-50"
            }`;

        item.onclick = () => {
            activeIndex = i;
            render();
        };

        const badge = isComplete

            ? `
                <div
                    class="w-7 h-7 rounded-lg bg-teal-600 text-white flex items-center justify-center text-xs shrink-0"
                >
                    <svg
                        class="w-4 h-4"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="3"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M5 13l4 4L19 7"
                        />
                    </svg>
                </div>
            `

            : `
                <div
                    class="w-7 h-7 rounded-lg ${isActive
                ? "bg-teal-700 text-white"
                : "bg-slate-100 text-slate-500"
            } flex items-center justify-center text-[11px] font-bold shrink-0"
                >
                    ${String(i + 1).padStart(2, "0")}
                </div>
            `;


        item.innerHTML = `

            ${badge}

            <div class="flex-1 min-w-0">

                <p
                    class="text-sm font-semibold text-slate-700 truncate"
                >
                    ${s.title}
                </p>

                <p
                    class="text-[11px] text-slate-400 mb-1"
                >
                    ${doneCount}/${total} item selesai
                </p>

                <div
                    class="w-full h-1 rounded-full bg-slate-100 overflow-hidden"
                >

                    <div
                        class="h-full bg-teal-600 rounded-full"
                        style="width:${pct}%"
                    ></div>

                </div>

            </div>

            <svg
                class="w-4 h-4 text-slate-300 shrink-0"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M9 5l7 7-7 7"
                />
            </svg>

        `;

        list.appendChild(item);

    });

}

function getStatusTarget(tanggalTarget) {
    if (!tanggalTarget) {
        return null;
    }

    const hariIni = new Date();
    const target = new Date(tanggalTarget);

    // Hilangkan jam agar perhitungan hanya berdasarkan tanggal
    hariIni.setHours(0, 0, 0, 0);
    target.setHours(0, 0, 0, 0);

    const selisihMs = target - hariIni;
    const sisaHari = Math.ceil(
        selisihMs / (1000 * 60 * 60 * 24)
    );

    if (sisaHari <= 3) {
        return {
            level: "tinggi",
            sisaHari: sisaHari,
            icon: "alert-triangle",
            className: "text-red-500",
            title:
                sisaHari < 0
                    ? `Terlambat ${Math.abs(sisaHari)} hari`
                    : sisaHari === 0
                        ? "Target hari ini"
                        : `Target ${sisaHari} hari lagi`
        };
    }

    if (sisaHari <= 7) {
        return {
            level: "sedang",
            sisaHari: sisaHari,
            icon: "alert-circle",
            className: "text-orange-500",
            title: `Target ${sisaHari} hari lagi`
        };
    }

    return null;
}

function renderDetail() {

    const s =
        stages[activeIndex];

    if (!s) {

        console.warn(
            "Tidak ada stage aktif"
        );

        return;
    }

    const detailTargetHari =
        document.getElementById("detail-target-hari");

    const detailTanggalTarget =
        document.getElementById("detail-tanggal-target");

    const detailTargetSeparator =
        document.getElementById("detail-target-separator");

    const detailTargetDateSeparator =
        document.getElementById("detail-target-date-separator");

    const punyaTarget =
        s.status &&
        s.status.target_hari &&
        s.status.tanggal_target;

    if (punyaTarget) {

        // Durasi
        detailTargetHari.textContent =
            `Target: ${s.status.target_hari} hari`;

        // Tanggal target
        detailTanggalTarget.textContent =
            formatTanggal(s.status.tanggal_target);

        // Tampilkan
        detailTargetHari.classList.remove("hidden");
        detailTanggalTarget.classList.remove("hidden");
        detailTargetSeparator.classList.remove("hidden");
        detailTargetDateSeparator.classList.remove("hidden");

    } else {

        // Sembunyikan semuanya
        detailTargetHari.classList.add("hidden");
        detailTanggalTarget.classList.add("hidden");
        detailTargetSeparator.classList.add("hidden");
        detailTargetDateSeparator.classList.add("hidden");
    }


    if (s.status && s.status.target_hari) {
        detailTargetHari.textContent =
            `Target: ${s.status.target_hari} hari`;
    } else {
        detailTargetHari.textContent =
            "Target: -";
    }

    if (s.status && s.status.tanggal_target) {
        detailTanggalTarget.textContent =
            formatTanggal(s.status.tanggal_target);
    } else {
        detailTanggalTarget.textContent =
            "-";
    }

    const detailTahap =
        document.getElementById(
            "detail-tahap"
        );

    const detailTitle =
        document.getElementById(
            "detail-title"
        );

    const detailSubtitle =
        document.getElementById(
            "detail-subtitle"
        );


    if (detailTahap) {

        detailTahap.textContent =
            `TAHAP ${String(
                activeIndex + 1
            ).padStart(2, "0")}`;
    }


    if (detailTitle) {

        detailTitle.textContent =
            s.title;

    }


    if (detailSubtitle) {

        detailSubtitle.textContent =
            s.subtitle;

    }

    const doneCount =
        s.items.filter(
            item => item.is_done
        ).length;

    const total =
        s.items.length;

    const statusEl =
        document.getElementById(
            "detail-status"
        );


    if (statusEl) {

        if (
            doneCount === total &&
            total > 0
        ) {

            statusEl.textContent =
                "Selesai";

            statusEl.className =
                "text-[11px] font-semibold px-2.5 py-1 rounded-full bg-teal-50 text-teal-700";

        }

        else if (
            doneCount === 0
        ) {

            statusEl.textContent =
                "Belum dimulai";

            statusEl.className =
                "text-[11px] font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-500";

        }

        else {

            statusEl.textContent =
                "Dalam proses";

            statusEl.className =
                "text-[11px] font-semibold px-2.5 py-1 rounded-full bg-amber-50 text-amber-600";

        }

    }

    const itemsWrap =
        document.getElementById(
            "detail-items"
        );


    if (!itemsWrap) {

        console.error(
            "#detail-items tidak ditemukan"
        );

        return;
    }

    itemsWrap.innerHTML = "";

    s.items.forEach((item, i) => {
        const isDone = Boolean(item.is_done);

        const row = document.createElement("div");

        row.className =
            "flex items-center gap-4 py-3 border-b border-slate-50 last:border-0";

        const punyaTarget =
            item.target_hari &&
            item.tanggal_target;

        const statusTarget =
            !isDone
                ? getStatusTarget(item.tanggal_target)
                : null;

        row.innerHTML = `
    <!-- Checkbox -->
    <button
        type="button"
        data-idx="${i}"
        class="checkbox-btn w-5 h-5 rounded border ${isDone
                ? "bg-teal-600 border-teal-600"
                : "border-slate-300"
            } flex items-center justify-center shrink-0"
    >
        ${isDone
                ? `
                    <svg
                        class="w-3.5 h-3.5 text-white"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="3"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M5 13l4 4L19 7"
                        />
                    </svg>
                `
                : ""
            }
    </button>

    <!-- Nomor -->
    <span
        class="text-[11px] font-semibold text-slate-400 w-6 shrink-0"
    >
        ${String(i + 1).padStart(2, "0")}
    </span>

    <!-- Nama + Target -->
    <div class="flex-1 min-w-0">

        <p
            class="text-sm ${isDone
                ? "text-slate-400 line-through"
                : "text-slate-700"
            }"
        >
            ${item.label}
        </p>

        ${punyaTarget
                ? `
                    <div class="flex items-center gap-2 mt-1">

                        <span class="text-[10px] text-slate-400">
                            ${item.target_hari} hari
                        </span>

                        <span class="text-slate-300 text-[10px]">
                            •
                        </span>

                        <span class="text-[10px] text-slate-400">
                            Target:
                            ${formatTanggal(item.tanggal_target)}
                        </span>

                        ${statusTarget
                    ? `
                                    <span
                                        class="flex items-center ml-1 ${statusTarget.className
                    }"
                                        title="${statusTarget.title
                    }"
                                    >
                                        <i
                                            data-lucide="${statusTarget.icon
                    }"
                                            class="w-3.5 h-3.5"
                                        ></i>
                                    </span>
                                `
                    : ""
                }

                    </div>
                `
                : ""
            }

    </div>

    <!-- Kalender -->
    <button
        type="button"
        class="btn-target-item
               w-8 h-8
               flex items-center justify-center
               rounded-lg
               text-slate-400
               hover:bg-slate-100
               hover:text-teal-600
               transition
               shrink-0"
        data-idx="${i}"
        title="Atur target persyaratan"
    >
        <i
            data-lucide="calendar-days"
            class="w-4 h-4"
        ></i>
    </button>
`;

        itemsWrap.appendChild(row);
    });

    lucide.createIcons();

    document
        .querySelectorAll(".checkbox-btn")
        .forEach(btn => {

            btn.onclick = async () => {

                const idx =
                    parseInt(
                        btn.dataset.idx
                    );


                const item =
                    s.items[idx];


                if (!item) {

                    console.error(
                        "Checklist item tidak ditemukan"
                    );

                    return;

                }


                const newStatus =
                    !item.is_done;


                console.log(
                    "CHECKLIST DIKLIK:",
                    item.id_checklist,
                    newStatus
                );


                try {

                    const response =
                        await fetch(
                            "/api/checklist/update",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify({
                                        id_checklist:
                                            item.id_checklist,

                                        is_done:
                                            newStatus
                                    })
                            }
                        );


                    const result =
                        await response.json();


                    console.log(
                        "UPDATE CHECKLIST:",
                        result
                    );


                    if (
                        !response.ok ||
                        !result.success
                    ) {

                        throw new Error(
                            result.message ||
                            "Gagal menyimpan checklist"
                        );

                    }

                    item.is_done =
                        Boolean(
                            result.is_done
                        );

                    syncChecklistToKontrakData(
                        s.id_document,
                        item.id_checklist,
                        item.is_done
                    );

                    render();
                }

                catch (error) {

                    console.error(
                        "Gagal menyimpan checklist:",
                        error
                    );


                    alert(
                        "Checklist gagal disimpan: " +
                        error.message
                    );

                }

            };

        });

    document
        .querySelectorAll(".btn-target-item")
        .forEach(btn => {

            btn.onclick = () => {

                const idx =
                    parseInt(btn.dataset.idx);

                const item =
                    s.items[idx];

                if (!item) {

                    console.error(
                        "Persyaratan tidak ditemukan"
                    );

                    return;
                }

                bukaModalTargetItem(item);
            };

        });

    const detailCount =
        document.getElementById(
            "detail-count"
        );


    if (detailCount) {

        detailCount.textContent =
            `${doneCount} dari ${total}`;

    }

}

function syncChecklistToKontrakData(
    idDocument,
    idChecklist,
    isDone
) {

    const kontrakId =
        parseInt(
            kontrakSelect.value
        );


    const dataKontrak =
        kontrakData.find(
            item =>
                Number(item.kontrak.id) ===
                Number(kontrakId)
        );


    if (!dataKontrak) {

        console.warn(
            "Data kontrak untuk sinkronisasi tidak ditemukan"
        );

        return;

    }


    const tahapan =
        dataKontrak.tahapan_data.find(
            tahapan =>
                Number(
                    tahapan.dokumen.id
                ) ===
                Number(idDocument)
        );


    if (!tahapan) {

        console.warn(
            "Tahapan untuk sinkronisasi tidak ditemukan"
        );

        return;

    }


    const checklist =
        tahapan.checklist_items.find(
            item =>
                Number(
                    item.id_checklist
                ) ===
                Number(idChecklist)
        );


    if (!checklist) {

        console.warn(
            "Checklist untuk sinkronisasi tidak ditemukan"
        );

        return;

    }


    checklist.is_done =
        Boolean(isDone);


    console.log(
        "KONTRAK DATA BERHASIL DISINKRONKAN:",
        checklist
    );

}

if (completeBtn) {

    completeBtn.type = "button";


    completeBtn.onclick =
        async () => {

            console.log(
                "================================="
            );

            console.log(
                "TANDAI TAHAP SELESAI"
            );

            console.log(
                "================================="
            );


            const s =
                stages[activeIndex];


            if (!s) {

                console.error(
                    "Tidak ada stage aktif"
                );

                return;

            }


            const kontrakId =
                parseInt(
                    kontrakSelect.value
                );


            console.log(
                "ID KONTRAK:",
                kontrakId
            );

            console.log(
                "ID DOCUMENT:",
                s.id_document
            );

            console.log(
                "JUMLAH CHECKLIST:",
                s.items.length
            );


            try {

                // ======================================
                // KIRIM REQUEST KE SERVER
                // ======================================

                const response =
                    await fetch(
                        "/api/tahapan/complete",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({

                                    id_kontrak:
                                        kontrakId,

                                    id_document:
                                        s.id_document

                                })
                        }
                    );


                const result =
                    await response.json();


                console.log(
                    "RESPONSE TANDAI TAHAP:",
                    result
                );


                if (
                    !response.ok ||
                    !result.success
                ) {

                    throw new Error(
                        result.message ||
                        "Gagal mencentang persyaratan"
                    );

                }

                s.items.forEach(
                    item => {

                        item.is_done =
                            true;

                    }
                );

                const dataKontrak =
                    kontrakData.find(
                        item =>
                            Number(
                                item.kontrak.id
                            ) ===
                            Number(kontrakId)
                    );


                if (dataKontrak) {

                    const tahapan =
                        dataKontrak.tahapan_data.find(
                            tahapan =>
                                Number(
                                    tahapan.dokumen.id
                                ) ===
                                Number(s.id_document)
                        );


                    if (tahapan) {

                        tahapan.checklist_items
                            .forEach(item => {

                                item.is_done =
                                    true;

                            });

                    }

                }

                render();


                console.log(
                    `✅ ${result.updated} persyaratan berhasil dicentang`
                );

            }

            catch (error) {

                console.error(
                    "❌ Gagal menandai tahap selesai:",
                    error
                );


                alert(
                    "Gagal mencentang persyaratan: " +
                    error.message
                );

            }

        };

} else {

    console.error(
        "❌ #complete-btn tidak ditemukan"
    );

}

function renderStats() {

    let done = 0;
    let total = 0;


    stages.forEach(s => {

        done +=
            s.items.filter(
                item => item.is_done
            ).length;


        total +=
            s.items.length;

    });


    const pct =
        total
            ? Math.round(
                (done / total) * 100
            )
            : 0;

    const statDone =
        document.getElementById(
            "stat-done"
        );

    const statTotal =
        document.getElementById(
            "stat-total"
        );


    const statRemaining =
        document.getElementById(
            "stat-remaining"
        );


    const statPercent =
        document.getElementById(
            "stat-percent"
        );


    const progressBar =
        document.getElementById(
            "progress-bar"
        );


    if (statDone) {
        statDone.textContent =
            done;
    }


    if (statTotal) {
        statTotal.textContent =
            total;
    }


    if (statRemaining) {
        statRemaining.textContent =
            total - done;
    }


    if (statPercent) {
        statPercent.textContent =
            pct + "%";
    }


    if (progressBar) {

        progressBar.style.width =
            pct + "%";

    }

}

function render() {

    console.log(
        "=== RENDER ==="
    );

    console.log(
        "Active index:",
        activeIndex
    );

    console.log(
        "Stages:",
        stages
    );


    renderSidebar();

    renderDetail();

    renderStats();

}

// Pilih kontrak pertama secara otomatis
if (
    kontrakSelect &&
    kontrakSelect.options.length > 1
) {

    kontrakSelect.selectedIndex = 1;

    const kontrakId =
        parseInt(
            kontrakSelect.value
        );

    if (kontrakId) {

        loadContractData(
            kontrakId
        );

    }

}

function bukaModalTarget() {

    // Ambil tahap yang sedang aktif
    const stage = stages[activeIndex];

    if (!stage) {
        console.error("Tahap aktif tidak ditemukan");
        return;
    }

    const status = stage.status;

    // Judul modal
    modalTargetTitle.textContent = stage.title;

    // Target hari
    if (status && status.target_hari) {
        modalTargetHari.value = status.target_hari;
    } else {
        modalTargetHari.value = "";
    }

    // Tanggal mulai
    if (status && status.tanggal_mulai) {

        modalTanggalMulai.textContent =
            formatTanggal(status.tanggal_mulai);

    } else {

        modalTanggalMulai.textContent =
            formatTanggalHariIni();

    }

    // Tanggal target
    if (status && status.tanggal_target) {

        modalTanggalTarget.textContent =
            formatTanggal(status.tanggal_target);

    } else {

        modalTanggalTarget.textContent = "-";

    }

    // Buka modal
    targetModal.classList.remove("hidden");
    targetModal.classList.add("flex");

    // Refresh icon Lucide
    lucide.createIcons();
}

function tutupModalTarget() {
    targetModal.classList.add("hidden");
    targetModal.classList.remove("flex");
}

btnTarget.addEventListener("click", bukaModalTarget);

btnCloseTarget.addEventListener("click", tutupModalTarget);

btnBatalTarget.addEventListener("click", tutupModalTarget);

document.getElementById("target-modal-overlay").addEventListener("click", tutupModalTarget);

modalTargetHari.addEventListener("input", function () {

    const targetHari = parseInt(this.value);

    if (!targetHari || targetHari <= 0) {
        modalTanggalTarget.textContent = "-";
        return;
    }

    const today = new Date();

    today.setDate(
        today.getDate() + targetHari
    );

    modalTanggalTarget.textContent =
        formatTanggalLocal(today);
});

function formatTanggalLocal(date) {

    return date.toLocaleDateString("id-ID", {
        day: "2-digit",
        month: "short",
        year: "numeric"
    });
}

function formatTanggal(tanggal) {

    if (!tanggal) {
        return "-";
    }

    const date = new Date(tanggal);

    return date.toLocaleDateString("id-ID", {
        day: "2-digit",
        month: "short",
        year: "numeric"
    });
}

function formatTanggalHariIni() {

    return formatTanggalLocal(
        new Date()
    );
}

btnSimpanTarget.addEventListener("click", async function () {

    const targetHari = parseInt(
        modalTargetHari.value
    );

    if (!targetHari || targetHari <= 0) {

        alert("Target hari harus diisi.");

        modalTargetHari.focus();

        return;
    }

    // Ambil tahap yang sedang aktif
    const stage = stages[activeIndex];

    if (!stage) {

        alert("Tahap aktif tidak ditemukan.");

        return;
    }

    if (!stage.status || !stage.status.id) {

        alert("Status tahapan tidak ditemukan.");

        return;
    }

    try {

        const response = await fetch(
            `/status-tahapan/${stage.status.id}/mulai`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    target_hari: targetHari
                })
            }
        );

        const result = await response.json();

        console.log("RESPONSE TARGET:", result);

        if (!response.ok || !result.success) {

            throw new Error(
                result.message ||
                "Gagal menyimpan target"
            );

        }

        stage.status.tanggal_mulai =
            result.tanggal_mulai;

        stage.status.target_hari =
            result.target_hari;

        stage.status.tanggal_target =
            result.tanggal_target;

        stage.status.tanggal_selesai =
            result.tanggal_selesai;

        tutupModalTarget();

        render();


    } catch (error) {

        console.error(
            "Gagal menyimpan target:",
            error
        );

        alert(
            "Gagal menyimpan target: " +
            error.message
        );

    }

});

function bukaModalTargetItem(item) {

    activeChecklistItem = item;

    if (!itemTargetModal) {

        console.error(
            "#item-target-modal tidak ditemukan"
        );

        return;
    }

    // Judul persyaratan
    itemTargetModalTitle.textContent =
        item.label;


    // Target hari
    if (item.target_hari) {

        itemTargetHari.value =
            item.target_hari;

    } else {

        itemTargetHari.value = "";

    }


    // Tanggal mulai
    if (item.tanggal_mulai) {

        itemTanggalMulai.textContent =
            formatTanggal(item.tanggal_mulai);

    } else {

        itemTanggalMulai.textContent =
            formatTanggalHariIni();

    }

    // Tanggal target
    if (item.tanggal_target) {

        itemTanggalTarget.textContent =
            formatTanggal(item.tanggal_target);

    } else {

        itemTanggalTarget.textContent =
            "-";
    }

    // Buka modal
    itemTargetModal.classList.remove("hidden");

    itemTargetModal.classList.add("flex");


    // Refresh Lucide
    lucide.createIcons();
}

function tutupModalTargetItem() {

    if (!itemTargetModal) {
        return;
    }

    itemTargetModal.classList.add("hidden");

    itemTargetModal.classList.remove("flex");

    activeChecklistItem = null;
}

if (btnCloseItemTarget) {

    btnCloseItemTarget.addEventListener(
        "click",
        tutupModalTargetItem
    );

}

if (btnBatalItemTarget) {

    btnBatalItemTarget.addEventListener(
        "click",
        tutupModalTargetItem
    );

}

if (itemTargetHari) {

    itemTargetHari.addEventListener(
        "input",
        function () {

            const targetHari =
                parseInt(this.value);

            if (
                !targetHari ||
                targetHari <= 0
            ) {

                itemTanggalTarget.textContent =
                    "-";

                return;
            }

            const tanggalMulai =
                activeChecklistItem &&
                    activeChecklistItem.tanggal_mulai
                    ? new Date(
                        activeChecklistItem.tanggal_mulai
                    )
                    : new Date();

            tanggalMulai.setDate(
                tanggalMulai.getDate() +
                targetHari
            );
            itemTanggalTarget.textContent =
                formatTanggalLocal(
                    tanggalMulai
                );
        }
    );

}

if (btnSimpanItemTarget) {
    btnSimpanItemTarget.addEventListener(
        "click",
        async function () {
            const targetHari =
                parseInt(
                    itemTargetHari.value
                );

            if (
                !targetHari ||
                targetHari <= 0
            ) {
                alert(
                    "Target hari harus diisi."
                );
                itemTargetHari.focus();
                return;
            }

            if (!activeChecklistItem) {
                alert(
                    "Persyaratan tidak ditemukan."
                );
                return;
            }

            try {
                const response =
                    await fetch(
                        `/item-checklist/${activeChecklistItem.id_checklist}/mulai`,
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({
                                    target_hari:
                                        targetHari
                                })
                        }
                    );

                const result =
                    await response.json();

                console.log(
                    "RESPONSE TARGET ITEM:",
                    result
                );


                if (
                    !response.ok ||
                    !result.success
                ) {
                    throw new Error(
                        result.message ||
                        "Gagal menyimpan target"
                    );
                }

                // Update state item
                activeChecklistItem.tanggal_mulai =
                    result.tanggal_mulai;

                activeChecklistItem.target_hari =
                    result.target_hari;

                activeChecklistItem.tanggal_target =
                    result.tanggal_target;

                activeChecklistItem.tanggal_selesai =
                    result.tanggal_selesai;

                // Tutup modal
                tutupModalTargetItem();

                // Render ulang
                render();

            }

            catch (error) {

                console.error(
                    "Gagal menyimpan target persyaratan:",
                    error
                );

                alert(
                    "Gagal menyimpan target persyaratan: " +
                    error.message
                );
            }
        }
    );

}