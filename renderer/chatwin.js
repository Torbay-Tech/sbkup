let closeChatWin = document.createElement('div')
closeChatWin.innerText = 'Close'

closeChatWin.style.position = 'fixed'
closeChatWin.style.bottom = '15px'
closeChatWin.style.right = '15px'
closeChatWin.style.padding = '5px 10px'
closeChatWin.style.fontSize = '20px'
closeChatWin.style.background = 'firebrick'
closeChatWin.style.color = 'white'
closeChatWin.style.borderRadius = '5px'
closeChatWin.style.cursor = 'default'
closeChatWin.style.boxShadow = '2px 2px 2px rgba(0,0,0,0.2)'
closeChatWin.style.zIndex = '9999'

closeChatWin.onclick = e => {
    window.opener.post('close-win', '*')
}

document.getElementsByTagName('body')[0].append(closeChatWin)