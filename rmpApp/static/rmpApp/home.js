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

for (const button of removeButtons) {
    button.addEventListener('click', () => {
        const index = teacherList.indexOf(button.id)
        if (index !== -1) {
            teacherList.splice(index, 1)
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
searchbutton.addEventListener('click', () => {
    searchPost();
});

searchform.addEventListener('submit', (e) => {
    e.preventDefault();
    searchPost();
});

const reviewXs = document.querySelectorAll('.reviewX');
console.log(reviewXs)
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

