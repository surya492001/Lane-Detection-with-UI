async function uploadVideo() {
    const input = document.getElementById('videoInput');
    if (input.files.length === 0) {
        alert("Please select a video file.");
        return;
    }

    const videoFile = input.files[0];
    const formData = new FormData();
    formData.append('video', videoFile);

    try {
        const response = await fetch('/process_frame', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);  // Log server response
            // Update UI or handle response as needed
        } else {
            console.error('Failed to process video:', response.status);
            alert('Failed to process video. Please try again later.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process video. Please check your network connection and try again.');
    }
}
