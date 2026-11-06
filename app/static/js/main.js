/**
 * ASM Transport Kebumen V2 - Public Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Calculate duration between departure & return date
    const depInput = document.getElementById('departure_date');
    const retInput = document.getElementById('return_date');
    const durationBadge = document.getElementById('durationBadge');

    function calculateDuration() {
        if (!depInput || !retInput) return;
        const depVal = depInput.value;
        const retVal = retInput.value;

        if (depVal && retVal) {
            const d1 = new Date(depVal);
            const d2 = new Date(retVal);
            const diffTime = d2.getTime() - d1.getTime();
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;

            if (durationBadge) {
                if (diffDays >= 1) {
                    durationBadge.innerHTML = `<i class="fa-solid fa-clock me-1"></i> Durasi: <strong>${diffDays} Hari</strong>`;
                    durationBadge.classList.remove('d-none', 'bg-danger-subtle', 'text-danger');
                    durationBadge.classList.add('bg-primary-subtle', 'text-primary');
                } else {
                    durationBadge.innerHTML = `<i class="fa-solid fa-triangle-exclamation me-1"></i> Tanggal pulang tidak boleh sebelum tanggal berangkat!`;
                    durationBadge.classList.remove('d-none', 'bg-primary-subtle', 'text-primary');
                    durationBadge.classList.add('bg-danger-subtle', 'text-danger');
                }
            }
        }
    }

    if (depInput && retInput) {
        depInput.addEventListener('change', function () {
            if (retInput.value && retInput.value < depInput.value) {
                retInput.value = depInput.value;
            }
            calculateDuration();
        });
        retInput.addEventListener('change', calculateDuration);
        calculateDuration();
    }

    // 2. Lightbox Modal for Gallery
    const galleryItems = document.querySelectorAll('.gallery-tile');
    const lightboxModal = document.getElementById('galleryLightboxModal');
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxTitle = document.getElementById('lightboxTitle');
    const lightboxCaption = document.getElementById('lightboxCaption');

    if (lightboxModal && galleryItems.length > 0) {
        const bsModal = new bootstrap.Modal(lightboxModal);
        galleryItems.forEach(item => {
            item.addEventListener('click', function () {
                const src = this.getAttribute('data-img');
                const title = this.getAttribute('data-title');
                const caption = this.getAttribute('data-caption');

                if (lightboxImg) lightboxImg.src = src;
                if (lightboxTitle) lightboxTitle.textContent = title || '';
                if (lightboxCaption) lightboxCaption.textContent = caption || '';

                bsModal.show();
            });
        });
    }

    // 3. Auto-dismiss alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 6000);
    });

    // 4. Navbar background shift on scroll
    const navbar = document.querySelector('.asm-navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 40) {
                navbar.style.boxShadow = '0 8px 30px rgba(0, 0, 0, 0.25)';
            } else {
                navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.12)';
            }
        });
    }
});

