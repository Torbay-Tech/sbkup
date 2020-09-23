let channels = document.getElementById('channels')

//Change on Keypress

exports.changeSelection = direction => {
    let currentChannel = document.getElementsByClassName('channel-item selected')[0]
    if (direction === 'ArrowUp' && currentChannel.previousElementSibling) {
        currentChannel.classList.remove('selected')
        currentChannel.previousElementSibling.classList.add('selected')
    } else if (direction === 'ArrowDown' && currentChannel.nextElementSibling) {
        currentChannel.classList.remove('selected')
        currentChannel.nextElementSibling.classList.add('selected')
    }
}

//Open the chat history
exports.open = () => {
    if ((document.getElementsByClassName('channel-item')).length === 0) return
    let selectedChannel = document.getElementsByClassName('channel-item selected')[0]

    let contentURL = selectedChannel.dataset.url

    console.log('opening...' + contentURL)
    //Open the chat in proxy browser window
    window.open(`${__dirname}/../mock/data/azureboards.html`,'')

}

exports.addChannel = channel => {
    let channelItem = document.createElement('div')

    channelItem.setAttribute('class', 'channel-item')

    if(channel.is_private)
        channelItem.innerHTML = `<img src="https://icons-for-free.com/iconfiles/png/512/privacy+private+protect+icon-1320196395146652063.png"><h2>${channel.name}</h2>`
    else
        channelItem.innerHTML = `<img src="https://www.iconfinder.com/data/icons/heroicons-ui/24/icon-hashtag-512.png"><h2>${channel.name}</h2>`

    let contentUrl = "./mock/data/" + channel.name + ".html"

    channelItem.setAttribute('data-url', contentUrl )

    channels.appendChild(channelItem)

    //single click select
    channelItem.addEventListener('click', this.select)
    //double click open
    channelItem.addEventListener('dblclick', this.open)

    if(document.getElementsByClassName('channel-item').length === 1) {
        channelItem.classList.add('selected')
    }
}

exports.select = e => {
    document.getElementsByClassName('channel-item selected')[0].classList.remove('selected')
    e.currentTarget.classList.add('selected')
}