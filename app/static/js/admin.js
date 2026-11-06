/**
 * ASM Transport Kebumen - Admin JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Mobile Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.admin-sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('show');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function (e) {
            if (window.innerWidth < 992 && !sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }

    // 2. Delete Form Confirmations
    const deleteForms = document.querySelectorAll('.form-delete-confirm');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const message = this.getAttribute('data-confirm-message') || 'Apakah Anda yakin ingin menghapus data ini? Tindakan ini tidak dapat dibatalkan.';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // 3. Image file input live preview
    const fileInputs = document.querySelectorAll('input[type="file"].image-preview-input');
    fileInputs.forEach(input => {
        input.addEventListener('change', function () {
            const previewTargetId = this.getAttribute('data-preview-target');
            const previewEl = document.getElementById(previewTargetId);
            if (previewEl && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    previewEl.src = e.target.result;
                    previewEl.classList.remove('d-none');
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    });
});

