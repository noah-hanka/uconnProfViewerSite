const reviewButtons = document.querySelectorAll('.reviewbutton');
const teacherList = JSON.parse(document.querySelector('#selectedTeachersJsonList').textContent)['list'];
const removeButtons = document.querySelectorAll('.removeteacherbutton');

let activereview = null;

for (const button of reviewButtons) {
    button.addEventListener('click', () => {
        let id = button.id;
        let teacherID = id.substring(0, id.indexOf('_reviewbutton'));
        const reviewContainer = document.getElementById(`${teacherID}_reviews`);
        reviewContainer.classList.toggle('hidden');
        activereview = reviewContainer;
        toggleReview();
    })
}

const professorContainer = document.querySelector('#professorContainer')
for (const button of removeButtons) {
    button.addEventListener('click', () => {
        const index = teacherList.indexOf(button.id)
        if (index !== -1) {
            teacherList.splice(index, 1)
        }
        if (teacherList.length === 0) {
            const noteachers = document.createElement('div');
            noteachers.innerText = 'you have no professors selected, start by searching for them up top';
            noteachers.id = 'noteachertext'
            professorContainer.appendChild(noteachers);
        }
        // removes teacher box
        const reviewdiv = document.getElementById(`${button.id}_reviews`);
        reviewdiv.remove()
        button.parentElement.parentElement.remove();
    })
}

const searchform = document.querySelector('#searchform');


function searchPost() {
    let teacherFormEl = document.querySelector('#teacherData');
    teacherFormEl.setAttribute('value', teacherList);
    searchform.submit();
}

const searchbutton = document.getElementById('searchbutton');
const loadingscreen = document.getElementById('loadingscreen');
const loadingtext = document.getElementById('loadingtext');
searchbutton.addEventListener('click', () => {
    loadingtext.innerText = 'searching for professors . . .';
    loadingscreen.classList.toggle('hidden');
    searchPost();
});

searchform.addEventListener('submit', (e) => {
    e.preventDefault();
    loadingtext.innerText = 'searching for professors . . .';
    loadingscreen.classList.toggle('hidden');
    searchPost();
});

const reviewXs = document.querySelectorAll('.reviewX');
for (const reviewX of reviewXs) {
    reviewX.addEventListener('click', (e) => {
        activereview.classList.toggle('hidden');
        toggleReview();
    });
}

function toggleReview() {
    reviewbackground.classList.toggle('hidden');
    document.body.classList.toggle('noscroll');
}



// loading screen --------------------------------------------------------------------

