const {ipcRenderer} = require('electron')
const channels = require('./channels')

let showModal = document.getElementById('show-modal'),
    closeModal = document.getElementById('close-modal'),
    modal = document.getElementById('modal'),
    addToken = document.getElementById('add-token'),
    token = document.getElementById('token'),
    search = document.getElementById('search'),
    reset = document.getElementById('reset')

//Search for a channel
search.addEventListener('keyup', e => {
    Array.from( document.getElementsByClassName('channel-item') ).forEach( channel => {
        let hasMatch = channel.innerText.toLowerCase().includes(search.value)
        channel.style.display = hasMatch ? 'flex' : 'none'
    })
})

//reset channels
reset.addEventListener('click', e => {
    var elements = document.getElementsByClassName('channel-item');
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
})

const toggleModalButtons = () => {
    if (addToken.disabled === true) {

        addToken.disabled = false
        addToken.style.opacity = 1
        addToken.innerText = 'Add Token'
        closeModal.style.display = 'inline'

    } else {
        addToken.disabled = true
        addToken.style.opacity = 0.5
        addToken.innerText = 'Adding ...'
        closeModal.style.display = 'none'
    }
}

//Navigate Items
document.addEventListener('keydown', e => {
    if(e.key === 'ArrowUp' || e.key === 'ArrowDown') {
        channels.changeSelection(e.key)
    }
})


showModal.addEventListener('click', ev => {
    modal.style.display = 'flex'
    token.focus()
    token.value = ""
})

closeModal.addEventListener('click', ev => {
    modal.style.display = 'none'
})

addToken.addEventListener('click', ev => {
    if(token.value) {
        ipcRenderer.send('new-token', token.value)
        toggleModalButtons()
    }
})

ipcRenderer.on('new-token-success', (e, channel_list) => {

    //Display the channel list received
    for(var i=0; i<channel_list.length; i++) {
        channels.addChannel(channel_list[i])
    }

    toggleModalButtons()
    modal.style.display = 'none'
})

token.addEventListener('keyup', ev => {
    if(ev.key === 'Enter') {
        addToken.click()
    }
})
