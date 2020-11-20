var CreatedOKLodop7766 = null, CLodopIsLocal;
window.readyDoneExeCount = window.readyDoneExeCount || 0;

var LOAD_LODOP_LATER_ROUTES = ['newDoctorStation/StationLayoutEdit', ];

function needCLodop() {
    try {
        var ua = navigator.userAgent;
        if (ua.match(/Windows\sPhone/i))
            return true;
        if (ua.match(/iPhone|iPod|iPad/i))
            return true;
        if (ua.match(/Android/i))
            return true;
        if (ua.match(/Edge\D?\d+/i))
            return true;

        var verTrident = ua.match(/Trident\D?\d+/i);
        var verIE = ua.match(/MSIE\D?\d+/i);
        var verOPR = ua.match(/OPR\D?\d+/i);
        var verFF = ua.match(/Firefox\D?\d+/i);
        var x64 = ua.match(/x64/i);
        if ((!verTrident) && (!verIE) && (x64))
            return true;
        else if (verFF) {
            verFF = verFF[0].match(/\d+/);
            if ((verFF[0] >= 41) || (x64))
                return true;
        } else if (verOPR) {
            verOPR = verOPR[0].match(/\d+/);
            if (verOPR[0] >= 32)
                return true;
        } else if ((!verTrident) && (!verIE)) {
            var verChrome = ua.match(/Chrome\D?\d+/i);
            if (verChrome) {
                verChrome = verChrome[0].match(/\d+/);
                if (verChrome[0] >= 41)
                    return true;
            }
        }
        return false;
    } catch (err) {
        return true;
    }
}

// 自定义弹框，下载
function showDownLoad(t) {
    var lodopTip = top.document.getElementById("lodop_print_body");
    lodopTip.style.opacity = '0';
    setTimeout(function() {
        lodopTip && top.document.body.removeChild(lodopTip);
    }, 1500);
}

function showDialog(text, url) {
    text = text || "打印控件未安装或需要升级，安装后请刷新页面。</br>如果已经安装最新版本,请启动后再刷新页面。";
    url = url || location.origin;
    var lodopTip = top.document.getElementById("lodop_print_body");
    if (lodopTip) {
        return
    }
    var box = document.createElement('div');
    box.style.transition = 'opacity 0.7s linear';
    box.style.opacity = '1';
    box.id = 'lodop_print_body';
    var dom = '<div id="lodop_print_mask" style="position: fixed; left: 0; top: 0; right: 0; bottom: 0; z-index: 10000"></div>' + '<div style="display: flex; justify-content: center;align-items: center; position: fixed; left: 0; top: 0; right: 0; bottom: 0; overflow-x: hidden;overflow-y: auto; z-index: 10001;">' + '<div style="background: #fff; border-radius: 5px; padding: 20px; box-shadow: 1px 0px 5px 2px #9e9e9e;border: 1px solid #9e9e9e;">' + '<div style="font-weight: 600;">' + text + '</div>' + '<div style="text-align: right;margin-top: 30px;">' + '<a onclick="window.frames.ifm2print.showDownLoad(1)" style="margin-right: 10px; color: #fff; background: #00B7EB;padding: 4px 16px; border-radius: 4px;" href="' + url + '/front/files/lodop.zip" target="_blank">下载</a>' + '<span onclick="window.frames.ifm2print.showDownLoad()" style="color: #fff; background: #00B7EB;padding: 4px 16px; border-radius: 4px;cursor:pointer">已安装</span>' + '</div>' + '</div>' + '</div>';
    box.innerHTML = dom;
    // top.document.body.appendChild(box);
}

function loadLodopScripts() {
    //====页面引用CLodop云打印必须的JS文件,用双端口(8000和18000）避免其中某个被占用：====
    if (needCLodop() && navigator.platform.indexOf('Win') == 0) {
        var src1 = "http://localhost:8000/CLodopfuncs.js?priority=1";
        var src2 = "http://localhost:18000/CLodopfuncs.js?priority=0";

        var head = document.head || document.getElementsByTagName("head")[0] || document.documentElement;
        var oscript, oscript2;
        // oscript = document.createElement("script");
        // oscript.src = src1;
        // head.insertBefore(oscript, head.firstChild);
        oscript = document.createElement("script");
        oscript.async = true;
        oscript.src = src2;
        oscript.onload = function() {
            if (typeof window.parent.ifm2printReadyCallback === 'function') {
                window.readyRace && window.parent.ifm2printReadyCallback(window.LODOP, window.CLODOP, window);
                window.readyRace = true;
                window.readyDoneExeCount++
            }
        }
        oscript.onerror = function() {
            oscript2 = document.createElement("script");
            oscript2.async = true;
            oscript2.src = src1;
            oscript2.onload = function() {
                if (typeof window.parent.ifm2printReadyCallback === 'function') {
                    window.readyRace && window.parent.ifm2printReadyCallback(window.LODOP, window.CLODOP, window);
                    window.readyRace = true;
                    window.readyDoneExeCount++
                }
            }
            oscript2.onerror = function() {
                showDialog('请确保已经安装lodop打印软件并已正常启动8000或18000端口')
            }
            head.insertBefore(oscript2, head.firstChild);
        }
        head.insertBefore(oscript, head.firstChild);
        CLodopIsLocal = !!((src1 + src2).match(/\/\/localho|\/\/127.0.0./i));
    }
}

if (LOAD_LODOP_LATER_ROUTES.some(el=>location.href.indexOf(el) >= 0)) {
    // 是稍后加载 LODOP 路由的一员的
    document.addEventListener('readystatechange', function() {
        if (document.readyState === 'complete') {
            loadLodopScripts();
        }
    });
} else {
    loadLodopScripts();
}

//====获取LODOP对象的主过程：====
function getLodop(oOBJECT, oEMBED) {
    var strHtmInstall = "<br><font color='#FF00FF'>打印控件未安装!点击这里<a href='install_lodop32.exe' target='_self'>执行安装</a>,安装后请刷新页面或重新进入。</font>";
    var strHtmUpdate = "<br><font color='#FF00FF'>打印控件需要升级!点击这里<a href='install_lodop32.exe' target='_self'>执行升级</a>,升级后请重新进入。</font>";
    var strHtm64_Install = "<br><font color='#FF00FF'>打印控件未安装!点击这里<a href='install_lodop64.exe' target='_self'>执行安装</a>,安装后请刷新页面或重新进入。</font>";
    var strHtm64_Update = "<br><font color='#FF00FF'>打印控件需要升级!点击这里<a href='install_lodop64.exe' target='_self'>执行升级</a>,升级后请重新进入。</font>";
    var strHtmFireFox = "<br><br><font color='#FF00FF'>（注意：如曾安装过Lodop旧版附件npActiveXPLugin,请在【工具】->【附加组件】->【扩展】中先卸它）</font>";
    var strHtmChrome = "<br><br><font color='#FF00FF'>(如果此前正常，仅因浏览器升级或重安装而出问题，需重新执行以上安装）</font>";
    var strCLodopInstall_1 = "<br><font color='#FF00FF'>Web打印服务CLodop未安装启动，点击这里<a href='CLodop_Setup_for_Win32NT.exe' target='_self'>下载执行安装</a>";
    var strCLodopInstall_2 = "<br>（若此前已安装过，可<a href='CLodop.protocol:setup' target='_self'>点这里直接再次启动</a>）";
    var strCLodopInstall_3 = "，成功后请刷新本页面。</font>";
    var strCLodopUpdate = "<br><font color='#FF00FF'>Web打印服务CLodop需升级!点击这里<a href='CLodop_Setup_for_Win32NT.exe' target='_self'>执行升级</a>,升级后请刷新页面。</font>";
    var LODOP;
    try {
        var ua = navigator.userAgent;
        var isIE = !!(ua.match(/MSIE/i)) || !!(ua.match(/Trident/i));
        if (needCLodop()) {
            try {
                LODOP = getCLodop();
            } catch (err) {}
            if (!LODOP && (document.readyState !== "complete" || window.readyDoneExeCount < 2)) {
                // window.LODOP&&!LODOP.webskt||LODOP.webskt.readyState!=1
                // alert("网页还没下载完毕，请稍等一下再操作.");
                return;
            }
            if (!LODOP) {
                // document.body.innerHTML = strCLodopInstall_1 + (CLodopIsLocal ? strCLodopInstall_2 : "") + strCLodopInstall_3 + document.body.innerHTML;
                showDialog("Web打印服务CLodop未安装启动。</br>若此前已安装过请再次启动，成功后请刷新本页面。")
                return;
            } else {
                if (CLODOP.CVERSION < "3.0.7.5") {
                    // document.body.innerHTML = strCLodopUpdate + document.body.innerHTML;
                    showDialog("Web打印服务CLodop需升级,升级后请刷新页面")
                }
                if (oEMBED && oEMBED.parentNode)
                    oEMBED.parentNode.removeChild(oEMBED);
                if (oOBJECT && oOBJECT.parentNode)
                    oOBJECT.parentNode.removeChild(oOBJECT);
            }
        } else {
            var is64IE = isIE && !!(ua.match(/x64/i));
            //=====如果页面有Lodop就直接使用，没有则新建:==========
            if (oOBJECT || oEMBED) {
                if (isIE)
                    LODOP = oOBJECT;
                else
                    LODOP = oEMBED;
            } else if (!CreatedOKLodop7766) {
                LODOP = document.createElement("object");
                LODOP.setAttribute("width", 0);
                LODOP.setAttribute("height", 0);
                LODOP.setAttribute("style", "position:absolute;left:0px;top:-100px;width:0px;height:0px;");
                if (isIE)
                    LODOP.setAttribute("classid", "clsid:2105C259-1E0C-4534-8141-A753534CB4CA");
                else
                    LODOP.setAttribute("type", "application/x-print-lodop");
                document.documentElement.appendChild(LODOP);
                CreatedOKLodop7766 = LODOP;
            } else
                LODOP = CreatedOKLodop7766;
            //=====Lodop插件未安装时提示下载地址:==========
            if ((!LODOP) || (!LODOP.VERSION)) {
                if (ua.indexOf('Chrome') >= 0)
                    // document.body.innerHTML = strHtmChrome + document.body.innerHTML;
                    showDialog("如果此前正常，仅因浏览器升级或重安装而出问题，需重新执行安装")
                if (ua.indexOf('Firefox') >= 0)
                    // document.body.innerHTML = strHtmFireFox + document.body.innerHTML;
                    // document.body.innerHTML = (is64IE ? strHtm64_Install : strHtmInstall) + document.body.innerHTML;
                    showDialog("打印控件未安装!")
                return LODOP;
            }
        }
        if (LODOP.VERSION < "6.2.2.6") {
            if (!needCLodop())
                // document.body.innerHTML = (is64IE ? strHtm64_Update : strHtmUpdate) + document.body.innerHTML;
                showDialog("打印控件需要升级!")
            return LODOP;
        }
        //===如下空白位置适合调用统一功能(如注册语句、语言选择等):==

        //=======================================================
        return LODOP;
    } catch (err) {
        console.error("getLodop出错:" + err);
    }
}
