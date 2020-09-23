// Modules
const {app, BrowserWindow, ipcMain} = require('electron')
const windowStateKeeper = require('electron-window-state')

const {PythonShell} = require('python-shell')

const fs = require('fs')
const ini = require('ini')

const configFile = 'config/secret.ini'

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

//Mockup Channel Data
const channels = require("./mock/channels.json")


ipcMain.on('new-token', (e, token) => {


  //  e.sender.send('new-token-success', channels)



    var config = ini.parse(fs.readFileSync(configFile, 'utf-8'))
    config.slack.authkey = token
    fs.writeFileSync('config/secret.ini', ini.stringify(config))

    PythonShell.run('./processor/main.py', null, function (err, output) {
      console.log(output)
    })


    e.sender.send('new-token-success', channels)

})
// Create a new BrowserWindow when `app` is ready
function createWindow () {

  //Configure Window State Keeper
  let state = windowStateKeeper({
    defaultHeight: 550, defaultWidth: 450
  })


  mainWindow = new BrowserWindow({
    x: state.x, y: state.y,
    width: state.width, height: state.height,
    minWidth: 450, maxWidth: 650, minHeight: 450, maxHeight: 650,
    webPreferences: {
      nodeIntegration: true
    }
  })

  // Load main.html into the new BrowserWindow
  mainWindow.loadFile('renderer/main.html')
  //mainWindow.loadFile('mock/data/azureboards.html')

  state.manage(mainWindow)

  // Open DevTools - Remove for PRODUCTION!
  mainWindow.webContents.openDevTools();

  // Listen for window being closed
  mainWindow.on('closed',  () => {
    mainWindow = null
  })
}

// Electron `app` is ready
app.on('ready', createWindow)

// Quit when all windows are closed - (Not macOS - Darwin)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

// When app icon is clicked and app is running, (macOS) recreate the BrowserWindow
app.on('activate', () => {
  if (mainWindow === null) createWindow()
})

