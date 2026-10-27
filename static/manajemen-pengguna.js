const USERS_API = "/api/users";

let selectedDeleteUserId = null;

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove("hidden");
    modal.classList.add("flex");
    document.body.classList.add("overflow-hidden");

    if (window.lucide) {
        lucide.createIcons();
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add("hidden");
    modal.classList.remove("flex");

    const editOpen = !document
        .getElementById("editUserModal")
        .classList.contains("hidden");

    const deleteOpen = !document
        .getElementById("deleteUserModal")
        .classList.contains("hidden");

    if (!editOpen && !deleteOpen) {
        document.body.classList.remove("overflow-hidden");
    }
}

function closeEditModal() {
    closeModal("editUserModal");
}

function closeDeleteModal() {
    closeModal("deleteUserModal");
    selectedDeleteUserId = null;
}

// Mendukung respons JSON API.
async function readApiResponse(response) {
    const text = await response.text();
    let data = {};

    try {
        data = text ? JSON.parse(text) : {};
    } catch {
        throw new Error("Respons server bukan JSON yang valid.");
    }

    if (!response.ok) {
        throw new Error(
            data.error || data.message ||
            `Permintaan gagal (${response.status}).`
        );
    }

    return data;
}


async function openEditModal(userId) {
    try {
        const response = await fetch(`${USERS_API}/${userId}`, {
            credentials: "same-origin"
        });

        const result = await readApiResponse(response);
        const user = result.user || result.data || result;

        document.getElementById("editUserId").value = user.id;
        document.getElementById("editNama").value =
            user.nama_lengkap || "";
        document.getElementById("editUsername").value =
            user.username || "";
        document.getElementById("editEmail").value =
            user.email || "";
        document.getElementById("editRole").value =
            (user.role || "USER").toUpperCase();
        document.getElementById("editStatus").value =
            String(Boolean(user.is_active));

        openModal("editUserModal");
    } catch (error) {
        alert("Gagal mengambil data pengguna: " + error.message);
    }
}

function openDeleteModal(userId, nama, username) {
    selectedDeleteUserId = userId;

    document.getElementById("deleteUserName").textContent =
        nama || "Pengguna";
    document.getElementById("deleteUserUsername").textContent =
        username ? "@" + username : "";

    openModal("deleteUserModal");
}

// Proses UPDATE
document.getElementById("editUserForm").addEventListener(
    "submit",
    async function (event) {
        event.preventDefault();

        const button = document.getElementById("saveUserButton");
        const userId = document.getElementById("editUserId").value;

        const payload = {
            nama_lengkap: document.getElementById("editNama").value.trim(),
            username: document.getElementById("editUsername").value.trim(),
            email: document.getElementById("editEmail").value.trim(),
            role: document.getElementById("editRole").value,
            is_active:
                document.getElementById("editStatus").value === "true"
        };

        button.disabled = true;
        button.textContent = "Menyimpan...";

        try {
            const response = await fetch(`${USERS_API}/${userId}`, {
                method: "PUT",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            await readApiResponse(response);

            closeEditModal();
            alert("Data pengguna berhasil diperbarui.");

            // Muat ulang tabel menggunakan fungsi yang sudah ada.
            await loadUsers();
        } catch (error) {
            alert("Gagal memperbarui pengguna: " + error.message);
        } finally {
            button.disabled = false;
            button.textContent = "Simpan Perubahan";
        }
    }
);

// Proses DELETE
async function confirmDeleteUser() {
    if (selectedDeleteUserId === null) {
        return;
    }

    const button = document.getElementById("confirmDeleteButton");
    button.disabled = true;
    button.textContent = "Menghapus...";

    try {
        const response = await fetch(
            `${USERS_API}/${selectedDeleteUserId}`,
            {
                method: "DELETE",
                credentials: "same-origin"
            }
        );

        await readApiResponse(response);

        closeDeleteModal();
        alert("Pengguna berhasil dihapus.");

        await loadUsers();
    } catch (error) {
        alert("Gagal menghapus pengguna: " + error.message);
    } finally {
        button.disabled = false;
        button.textContent = "Ya, Hapus";
    }
}

// Tutup modal jika pengguna menekan Escape.
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeEditModal();
        closeDeleteModal();
    }
});