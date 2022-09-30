/**

 author:  jackkweyunga

 **/

let transcode_progress_list_id = "transcode_progress_list"
let transcode_progress_id = "transcode_progress"
let video_details_id = "video_details"


document.addEventListener('DOMContentLoaded', function () {
    const webSocketBridge = new channels.WebSocketBridge();

    webSocketBridge.connect(`/video_notifier/${user_id}/`);
    webSocketBridge.listen(function (action) {
        recordProgress(action);
    })

    document.ws = webSocketBridge;
})


function recordProgress(obj) {
    console.log("obj: ", obj)
    let vid = getVideoDetails(obj.id);


    if (vid !== null) {
        console.log("GotVideo: ", vid)
        updateProgress(obj.id, obj.per, obj.time_left)
        return true
    } else {
        console.log("GetVideoDetails: Adding video progress")
        if (Number(obj.per) === 100) {
            finishTranscoding(obj.id);
            return false
        }
        appendVideoToList(obj.id, obj.name, obj.time_left);
        return true
    }
}


function appendVideoToList(id, name, time_left) {
    let vpid = `${video_details_id}_${id}`;
    let vpgid = `${transcode_progress_id}_${id}`;
    let vpgtid = `${transcode_progress_id}_time_${id}`;

    let html = `
        <div class="container mt-3 mb-3" id="${vpid}">
            <p>${name}</p>
            <div class="d-flex w-100 align-items-center">
                <div class="progress w-100">
                    <div id="${vpgid}" class="progress-bar" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">0%</div>             
                </div>
                <span id="${vpgtid}" class="mx-3">${time_left}</span>
            </div>
        </div>
    `
    getProgressList().innerHTML += html;
}

function getVideoDetails(id) {
    return document.getElementById(`${video_details_id}_${id}`)
}

function finishTranscoding(id) {
    let vd = getVideoDetails(id);
    vd.hidden = true;
}

function getProgressList() {
    return document.getElementById(transcode_progress_list_id)
}

function updateProgress(id, per, time_left) {
    let vp = document.getElementById(`${transcode_progress_id}_${id}`)
    let vptl = document.getElementById(`${transcode_progress_id}_time_${id}`)
    vptl.innerText = time_left;
    vp.style.width = `${per}%`;
    vp.setAttribute("aria-valuenow", per)
    vp.innerText = `${per}%`;
}

