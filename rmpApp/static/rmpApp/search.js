const teachersJSON = JSON.parse(document.querySelector('#searchResults').textContent);
const initialTeachers = JSON.parse(document.querySelector('#selectedTeachersJsonList').textContent)['list'];
const compareList = document.querySelector('#compareList');
const addButtons = document.querySelectorAll('.addButton');


for (const teacher of initialTeachers) {
    const button = document.querySelector(`#${teacher}`);
    if (button !== null) {
        button.innerText = 'Remove Teacher from Compare List'
        button.classList.toggle('addedTeacher')
    }
}

function updateTeacherListButton(button) {
    const innerText = button.innerText;
    if (innerText === 'Add Teacher to Compare List') {
        button.innerText = 'Remove Teacher from Compare List'
        const new_li = document.createElement('li');
        new_li.classList.add('compare-li');
        let id_string = `${button.id}_li`;
        console.log(id_string)
        new_li.id = id_string;
        const teacher = teachersJSON[button.id]
        new_li.innerText = `${teacher["firstName"]} ${teacher['lastName']}`;
        compareList.appendChild(new_li);
    } else {
        button.innerText = 'Add Teacher to Compare List';
        let id_string = `${button.id}_li`;
        const li = document.querySelector(`#${id_string}`);
        li.remove()
    }
    button.classList.toggle('addedTeacher')

}


for (const button of addButtons) {
    button.addEventListener('click', (e) => {
        updateTeacherListButton(button);
    });
}