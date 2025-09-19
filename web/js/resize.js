window.addEventListener('pywebviewready', () => {
    let activeHandle = null;
    let initialMouseX = 0;
    let initialMouseY = 0;
    let initialWidth = 0;
    let initialHeight = 0;

    function onMouseDown(e, handle) {
        activeHandle = handle;
        initialMouseX = e.clientX;
        initialMouseY = e.clientY;
        initialWidth = window.innerWidth;
        initialHeight = window.innerHeight;
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
        e.preventDefault();
    }

    function onMouseMove(e) {
        if (!activeHandle) return;

        const dx = e.clientX - initialMouseX;
        const dy = e.clientY - initialMouseY;

        let newWidth = initialWidth;
        let newHeight = initialHeight;

        if (activeHandle.includes('e')) {
            newWidth = initialWidth + dx;
        }
        if (activeHandle.includes('s')) {
            newHeight = initialHeight + dy;
        }

        // Clamp to min_size (approximated from app.py)
        newWidth = Math.max(400, newWidth);
        newHeight = Math.max(300, newHeight);

        pywebview.api.resize(Math.round(newWidth), Math.round(newHeight));
    }

    function onMouseUp() {
        activeHandle = null;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }

    const handleSE = document.getElementById('resize_handle_se');
    const handleE = document.getElementById('resize_handle_e');
    const handleS = document.getElementById('resize_handle_s');

    if (handleSE) handleSE.addEventListener('mousedown', (e) => onMouseDown(e, 'se'));
    if (handleE) handleE.addEventListener('mousedown', (e) => onMouseDown(e, 'e'));
    if (handleS) handleS.addEventListener('mousedown', (e) => onMouseDown(e, 's'));

    // Window controls
    const minimizeBtn = document.getElementById('minimize_btn');
    const maximizeBtn = document.getElementById('maximize_btn');
    const closeBtn = document.getElementById('close_btn');

    if (minimizeBtn) minimizeBtn.addEventListener('click', () => pywebview.api.minimize());
    if (maximizeBtn) maximizeBtn.addEventListener('click', () => pywebview.api.toggle_maximize());
    if (closeBtn) closeBtn.addEventListener('click', () => pywebview.api.close());
});
