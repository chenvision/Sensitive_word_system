document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('detectForm');
    const resultDiv=document.getElementById('result');

    form.addEventListener('submit', function (event)  {
        event.preventDefault();
        const textInput=document.getElementById('textInput').value;

        fetch('api/detect',{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({text:textInput}),
            })
            .then(response => response.json())
            .then(data=>{
                const detectedWords=data.detected_words;
                resultDiv.innerHTML=`Detected sensitive words: ${detectedWords.join(', ')}`;
            })
            .catch(error => {
                cosole.error('Error:',error);
            });
    });
});