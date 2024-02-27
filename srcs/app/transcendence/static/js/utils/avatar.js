export function changeAvatar() {
    const avatar = document.getElementById('avatar');
    if (!avatar) { return; }

    avatar.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (!(file instanceof Blob)) { return; }

        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('avatar-preview');
            if (preview) {
                preview.src = e.target.result;
            }
        }
        reader.readAsDataURL(file);
    });
}