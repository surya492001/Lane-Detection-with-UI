async function uploadVideo() {
    const input = document.getElementById('videoInput');
    if (input.files.length === 0) {
        alert("Please select a video file.");
        return;
    }

    const videoFile = input.files[0];
    const formData = new FormData();
    formData.append('video', videoFile);

    const response = await fetch('/process_frame', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let buffer = '';

        reader.read().then(function processText({ done, value }) {
            if (done) {
                console.log("Stream complete");
                return;
            }
            buffer += decoder.decode(value, { stream: true });

            const boundary = buffer.indexOf('\r\n\r\n');
            if (boundary !== -1) {
                const frameData = buffer.slice(0, boundary);
                buffer = buffer.slice(boundary + 4);

                const base64Image = 'data:image/jpeg;base64,' + btoa(frameData);
                document.getElementById('frame').src = base64Image;
            }
            reader.read().then(processText);
        });
    } else {
        alert("Failed to process video");
    }
}
