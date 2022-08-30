const reviewButtons = document.querySelectorAll('.reviewbutton');
const teacherList = JSON.parse(document.querySelector('#selectedTeachersJsonList').textContent)['list'];
const removeButtons = document.querySelectorAll('.removeteacherbutton');


for (const button of reviewButtons) {
    button.addEventListener('click', () => {
        let id = button.id;
        const reviewContainer = document.getElementById(`${id}_reviews`);
        reviewContainer.style.visibility = 'visible';
    })
}

for (const button of removeButtons) {
    button.addEventListener('click', () => {
        const index = teacherList.indexOf(button.id)
        if (index !== -1) {
            teacherList.splice(index, 1)
        }
        // removes teacher box
        button.parentElement.parentElement.remove();
    })
}

function searchPost() {
    const form = document.querySelector('#searchform');
    console.log(form.id)
    let teacherFormEl = document.querySelector('#teacherData');
    teacherFormEl.setAttribute('value', teacherList);
    console.log(teacherList);
    form.submit();
}

const searchbutton = document.getElementById('searchbutton');
searchbutton.addEventListener('click', () => {
    searchPost();
});