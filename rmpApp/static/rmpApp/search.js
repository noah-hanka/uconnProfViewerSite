const teachersJSON = JSON.parse(document.querySelector('#searchResults').textContent);
const initialTeachers = JSON.parse(document.querySelector('#selectedTeachersJsonList').textContent)['list'];
const teacherList = initialTeachers

const compareList = document.querySelector('#compareList');
const addButtons = document.querySelectorAll('.addButton');
let removeButtons = document.querySelectorAll('.compare-li-button');

for (const teacher of initialTeachers) {
    const button = document.getElementById(`${teacher}`);
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
        new_li.id = id_string;
        const teacher = teachersJSON[button.id];

        const namediv = document.createElement('div');
        namediv.classList.add('compare-li-name')
        namediv.innerText = `${teacher["firstName"]} ${teacher['lastName']}`;
        new_li.appendChild(namediv);

        const removediv = document.createElement('div');
        const xdiv = document.createElement('div');
        xdiv.innerText = 'X';
        removediv.appendChild(xdiv);
        removediv.classList.add('compare-li-button');
        removediv.id = `${button.id}_removeButton`;
        new_li.appendChild(removediv);
        compareList.appendChild(new_li);
        teacherList.push(button.id)
    } else {
        button.innerText = 'Add Teacher to Compare List';
        let id_string = `${button.id}_li`;
        const li = document.getElementById(`${id_string}`);
        li.remove()
        const index = teacherList.indexOf(button.id)
        if (index !== -1) {
            teacherList.splice(index, 1)
        }
    }
    removeButtons = document.querySelectorAll('.compare-li-button');
    updateRemoveEventListeners();
    button.classList.toggle('addedTeacher')

}


for (const button of addButtons) {
    button.addEventListener('click', (e) => {
        updateTeacherListButton(button);

    });
}




function postTeachers() {
    const form = document.querySelector('#homeform');
    let teacherFormEl = document.querySelector('#homedata');
    teacherFormEl.setAttribute('value', teacherList);
    form.submit();
}

const inp = document.querySelector('#homesubmit');

inp.addEventListener('click', () => {
    postTeachers()
})


function updateRemoveEventListeners() {
    for (const removebutton of removeButtons) {
        removebutton.addEventListener('click', () => {
            const id = removebutton.id;
            const index = id.indexOf('_removeButton');
            const button = document.getElementById(id.substring(0, index));
            if (button) {
                updateTeacherListButton(button);
            } else {
                removebutton.parentElement.remove()
            }

        })
    }
}
updateRemoveEventListeners();


function searchPost() {
    const form = document.querySelector('#searchform');
    let teacherFormEl = document.querySelector('#teacherData');
    teacherFormEl.setAttribute('value', teacherList);
    form.submit();
}

const searchbutton = document.getElementById('searchbutton');
searchbutton.addEventListener('click', () => {
    searchPost();
});