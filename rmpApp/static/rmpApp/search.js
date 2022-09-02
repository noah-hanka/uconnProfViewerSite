const teachersJSON = JSON.parse(document.querySelector('#searchResults').textContent);
const initialTeachers = JSON.parse(document.querySelector('#selectedTeachersJsonList').textContent)['list'];
const teacherList = initialTeachers

const body = document.body;

const compareList = document.querySelector('#compareList');
const addButtons = document.querySelectorAll('.addButton');
const removeButtons = document.querySelectorAll('.compare-li-button');

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
        if (teacherList.length === 8) {
            toggleAlert();
            return;
        }
        button.innerText = 'Remove Teacher from Compare List'
        const new_li = document.createElement('li');
        new_li.classList.add('compare-li');
        let id_string = `${button.id}_li`;
        new_li.id = id_string;
        const teacher = teachersJSON[button.id];

        const namediv = document.createElement('div');
        namediv.classList.add('compare-li-name')
        namediv.innerText = `${teacher["firstName"]} ${teacher['lastName']}`.toLowerCase();
        new_li.appendChild(namediv);

        const removediv = document.createElement('div');
        removediv.innerText = 'X';
        removediv.classList.add('compare-li-button');
        removediv.id = `${button.id}_removeButton`;
        removediv.addEventListener('click', removeButtonListener);
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
    button.classList.toggle('addedTeacher')
    return;
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
    loadingtext.innerText = 'fetching selected professor reviews . . .';
    loadingscreen.classList.toggle('hidden');
    postTeachers()
})


for (const removebutton of removeButtons) {
    removebutton.addEventListener('click', removeButtonListener);
}

function removeButtonListener(e) {
    const removebutton = e.target;
    const teacherID = removebutton.id.substring(0, removebutton.id.indexOf('_removeButton'));
    const button = document.getElementById(teacherID);
    const index = teacherList.indexOf(teacherID);
    if (index !== -1) {
        teacherList.splice(index, 1)
    }
    if (button) {
        updateTeacherListButton(button);
    } else {
        removebutton.parentElement.remove();
    }
}

const searchform = document.querySelector('#searchform');
const loadingscreen = document.getElementById('loadingscreen');
const loadingtext = document.getElementById('loadingtext');


function searchPost() {
    let teacherFormEl = document.querySelector('#teacherData');
    teacherFormEl.setAttribute('value', teacherList);
    searchform.submit();
}

const searchbutton = document.getElementById('searchbutton');
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



const alertbackground = document.querySelector('#alertbackground');

function toggleAlert() {
    alertbackground.classList.toggle('hidden');
    body.classList.toggle('noscroll');
}

const alertok = document.querySelector('#alertbutton');
alertok.addEventListener('click', toggleAlert);



