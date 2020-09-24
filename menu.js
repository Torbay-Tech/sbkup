const {Menu} = require('electron')
const {shell} = require('electron')

module.exports = appWin => {

    let template = [
        {
            label: 'Channels',
            submenu: [
                {
                    label: 'Add Token',
                    accelerator: 'CmdOrCtrl+O',
                    click: () => {
                        appWin.send('menu-add-token')
                    }
                },
                {
                    label: 'Read Channel',
                    accelerator: 'CmdOrCtrl+Enter',
                    click: () => {
                        appWin.send('menu-read-channel')
                    }
                },
                {
                    label: 'Download',
                    accelerator: 'CmdOrCtrl+D',
                    click: () => {
                        appWin.send('menu-download-channel')
                    }
                },
                {
                    label: 'Search',
                    accelerator: 'CmdOrCtrl+S',
                    click: () => {
                        appWin.send('menu-search')
                    }
                }
            ]
        },
        {
            role: 'editMenu'
        },
        {
            role: 'windowMenu'
        },
        {
            role: 'help',
            submenu: [
                {
                    label: 'Learn More',
                    click: () => {
                        shell.openExternal("https://www.google.com")
                    }
                }
            ]
        }
    ]

    //Check Platform

    if (process.platform === 'darwin') template.unshift({ role: 'appMenu'})

    let menu = Menu.buildFromTemplate(template)

    Menu.setApplicationMenu(menu)
}