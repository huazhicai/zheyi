!function() {
    "use strict";
    function t(t, e) {
        window.requestIdleCallback ? requestIdleCallback(t, {
            timeout: e || 1e3
        }) : setTimeout(t, 0)
    }
    function e(t) {
        "complete" === document.readyState ? t() : window.addEventListener("load", t)
    }
    var n = function(t) {
        return ("" + (t || 0)).split(".")[0]
    };
    function o(t) {
        var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 1e3;
        if (!t)
            return "";
        var n = String(t);
        return n.length < e ? n : n.substr(0, e) + "..."
    }
    var i = document.getElementById("seenew-felog")
      , r = "felogs"
      , s = "felogs"
      , a = "cn-hangzhou.log.aliyuncs.com"
      , c = ""
      , d = "";
    function u() {
        d ? this.path_ = this.slsUrl = d : (this.path_ = "/logstores/" + s + "/track?APIVersion=0.6.0",
        this.slsUrl = "//" + r + "." + a + this.path_),
        this.uri_ = c ? this.path_ : this.slsUrl,
        this.params_ = new Array,
        this.httpRequest_ = window.ActiveXObject ? new ActiveXObject("Microsoft.XMLHTTP") : window.XMLHttpRequest ? new XMLHttpRequest : void 0,
        this.httpRequest_.timeout = 3e3
    }
    i && (r = i.getAttribute("data-project") || "felogs",
    s = i.getAttribute("data-logstore") || "felogs",
    a = i.getAttribute("data-host") || "cn-hangzhou.log.aliyuncs.com",
    c = i.getAttribute("data-cdn") || "",
    d = i.getAttribute("data-track") || ""),
    u.prototype = {
        push: function(t, e) {
            t && e && (this.params_.push(t),
            this.params_.push(e))
        },
        switchUrl: function() {
            this.uri_ == this.slsUrl ? this.uri_ = this.path_ : this.uri_ = this.slsUrl
        },
        checkNetWork: function() {
            var t = this;
            this.httpRequest_.onerror = function() {
                t.switchUrl()
            }
            ,
            this.httpRequest_.open("OPTIONS", this.uri_, !0),
            this.httpRequest_.send(null)
        },
        logger: function(t) {
            var e = this;
            if (!window.FELOG_DISABLE_TRACK) {
                for (var n = this.uri_, o = 0; this.params_.length > 0; )
                    n += o % 2 == 0 ? "&" + encodeURIComponent(this.params_.shift()) : "=" + encodeURIComponent(this.params_.shift()),
                    ++o;
                try {
                    this.httpRequest_.open("GET", n, !0),
                    this.httpRequest_.onerror = function(t) {
                        e.switchUrl(),
                        errCb && errCb()
                    }
                    ,
                    this.httpRequest_.ontimeout = function(t) {
                        e.switchUrl(),
                        errCb && errCb()
                    }
                    ,
                    this.httpRequest_.onload = function() {
                        this.status >= 200 && this.status <= 300 || 304 == this.status || t && t()
                    }
                    ,
                    this.httpRequest_.send(null)
                } catch (t) {
                    console.log(t)
                }
            }
        },
        loggerp: function(t, e, n) {
            var o = this;
            if (!window.FELOG_DISABLE_TRACK) {
                var i, r = this.uri_;
                try {
                    var s = "";
                    s = d ? JSON.stringify({
                        createDate: (i = new Date,
                        i.getFullYear() + "-" + (i.getMonth() + 1) + "-" + i.getDate() + " " + i.getHours() + ":" + i.getMinutes() + ":" + i.getSeconds()),
                        logType: 1,
                        device: "PC",
                        region: "",
                        tag: "",
                        ua: navigator.userAgent,
                        data: JSON.stringify(t)
                    }) : JSON.stringify({
                        __logs__: t
                    }),
                    this.httpRequest_.open("POST", r.split("?")[0], !0),
                    this.httpRequest_.setRequestHeader("Content-Type", "application/json;charset=UTF-8"),
                    this.httpRequest_.setRequestHeader("x-log-apiversion", "0.6.0"),
                    this.httpRequest_.setRequestHeader("x-log-bodyrawsize", s.length),
                    this.httpRequest_.onerror = function() {
                        o.switchUrl(),
                        n && n()
                    }
                    ,
                    this.httpRequest_.ontimeout = function(t) {
                        o.switchUrl(),
                        n && n()
                    }
                    ;
                    var a = this;
                    this.httpRequest_.onload = function() {
                        this.status >= 200 && this.status <= 300 || 304 == this.status ? e && e() : (a.switchUrl(),
                        n && n())
                    }
                    ,
                    this.httpRequest_.send(s)
                } catch (t) {
                    console.log(t)
                }
            }
        }
    };
    var f, h = void 0 !== document.hidden ? {
        hidden: "hidden",
        visibilityChange: "visibilitychange"
    } : void 0 !== document.webkitHidden ? {
        hidden: "webkitHidden",
        visibilityChange: "webkitvisibilitychange"
    } : void 0 !== document.msHidden ? {
        hidden: "msHidden",
        visibilityChange: "msvisibilitychange"
    } : void 0, l = !!h, p = function(t, e) {
        var n;
        l && document.addEventListener(h.visibilityChange, n = function(o) {
            e && document.removeEventListener(h.visibilityChange, n),
            t(!document[h.hidden])
        }
        )
    }, g = Object.assign || function(t) {
        for (var e = 1; e < arguments.length; e++) {
            var n = arguments[e];
            for (var o in n)
                Object.prototype.hasOwnProperty.call(n, o) && (t[o] = n[o])
        }
        return t
    }
    , v = (f = location.hostname).match(/test/) ? "test" : f.match(/dev|emr|t-his/) ? "dev" : f.match(/yb/) ? "yb" : f.match(/tt/) ? "tt" : f;
    window.FELOG = {
        env: v
    },
    window.performance && performance.timing && 0 !== performance.timing.navigationStart && (FELOG.navigationStart = performance.timing.navigationStart),
    FELOG.logger = FELOG.logger || new u,
    FELOG.queue = [];
    var w = function() {
        var t = sessionStorage.getItem("userID")
          , e = sessionStorage.getItem("userName")
          , n = sessionStorage.getItem("location")
          , o = location.search.split("-")[1]
          , i = sessionStorage.getItem("institutions")
          , r = sessionStorage.getItem("hospitalDistrictId");
        return {
            ti: document.title.replace(/(^\s+)|(\s+$)/g, ""),
            url: location.href,
            ts: Date.now(),
            user: t + "@" + e,
            loc: n + "@" + o,
            his: i + "@" + r,
            env: v
        }
    };
    FELOG._send = function(t) {
        var e = this;
        if (t) {
            var n = g({}, w(), t);
            Object.keys(n).forEach((function(t) {
                FELOG.logger.push(t, n[t])
            }
            )),
            FELOG.logger.logger((function() {
                e._waitSend(t)
            }
            ))
        }
    }
    ,
    FELOG._sendAll = function(t, e) {
        var n = this;
        if (this.queue.length) {
            var o = {}
              , i = this.queue.map((function(t) {
                return o = g({}, t),
                Object.keys(o).forEach((function(t) {
                    o[t] = String(o[t])
                }
                )),
                o
            }
            ));
            window.FELOG_DISABLE_UPLOAD_LOG ? (console.log("FELOG_DISABLE_UPLOAD_LOG", i),
            this.queue = [],
            t && t()) : FELOG.logger.loggerp(i, (function() {
                n.queue = [],
                t && t()
            }
            ), e)
        }
    }
    ;
    var m = 5e3;
    FELOG.uploadLog = function() {
        var e = setTimeout((function() {
            FELOG.blank && FELOG.blank(),
            FELOG.queue.length > 0 && t((function() {
                FELOG._sendAll((function() {
                    m = 5e3
                }
                ), (function() {
                    (m += 3e3) > 15e3 && (FELOG.queue = [])
                }
                )),
                function(t, e) {
                    var n, o, i, r = 0;
                    if ("utf-16" === (e = e ? e.toLowerCase() : "") || "utf16" === e)
                        for (o = 0,
                        i = t.length; o < i; o++)
                            r += (n = t.charCodeAt(o)) <= 65535 ? 2 : 4;
                    else
                        for (o = 0,
                        i = t.length; o < i; o++)
                            r += (n = t.charCodeAt(o)) <= 127 ? 1 : n <= 2047 ? 2 : n <= 65535 ? 3 : 4;
                    return r
                }(JSON.stringify(FELOG.queue)) > 1e6 && (FELOG.queue = [])
            }
            )),
            clearTimeout(e),
            FELOG.uploadLog()
        }
        ), m)
    }
    ,
    e((function() {
        FELOG.uploadLog(),
        p((function(t) {
            t || (console.log("leave page send felog"),
            FELOG._sendAll())
        }
        ))
    }
    ));
    FELOG._waitSend = function(t) {
        if (!(this.queue.length >= 200)) {
            var e = g({}, w(), t);
            this.queue.push(e)
        }
    }
    ,
    FELOG.send = function(t, e) {
        e ? this._send(t) : this._waitSend(t)
    }
    ;
    var L = function(t) {
        return t.reverse().filter((function(t) {
            return t !== window && t !== document
        }
        )).map((function(t) {
            return t.id ? "#" + t.id : t.className && "string" == typeof t.className ? "." + t.className.split(" ").filter((function(t) {
                return !!t
            }
            )).join(".") : t.nodeName
        }
        )).join(" ")
    };
    function E(t) {
        if (!t)
            return "";
        if ("[object Array]" === Object.prototype.toString.apply(t))
            return L(t);
        for (var e = [], n = t; n; )
            e.push(n),
            n = n.parentNode;
        return L(e)
    }
    var O = void 0;
    function y() {
        return O
    }
    ["pointerdown", "touchstart", "mousedown", "keydown", "mouseover"].forEach((function(t) {
        document.addEventListener(t, (function(t) {
            O = t
        }
        ), {
            capture: !0,
            passive: !0
        })
    }
    ));
    var G = Number.MAX_VALUE
      , F = EventTarget.prototype.addEventListener;
    function _(t, e) {
        return (void 0 === e || 200 === e) && (void 0 !== t.code ? 2e3 == t.code || 200 == t.code : void 0 !== t.status ? 200 == t.status : void 0 === t.message || "success" == t.message)
    }
    EventTarget.prototype.addEventListener = function(t, e, n) {
        try {
            return F.call(this, t, e, n)
        } catch (t) {
            throw t
        }
    }
    ,
    FELOG.request = function(t, e) {
        var n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {};
        if (!t.match("data:")) {
            var i = n.status
              , r = void 0 === i ? "" : i
              , s = n.code
              , a = void 0 === s ? "" : s
              , c = n.traceId
              , d = void 0 === c ? "" : c
              , u = n.duration
              , f = void 0 === u ? "" : u
              , h = n.msg
              , l = void 0 === h ? "" : h
              , p = n.body
              , g = void 0 === p ? "" : p
              , v = n.params
              , w = void 0 === v ? "" : v;
            g && (l = l + "-" + JSON.stringify(g).replace(/"[^"]+":null,?/g, "").replace(/"[^"]+":"null",?/g, "").replace(/null,?/g, ""));
            var m = f > window.FELOG_MAX_API_LATENCY || Math.random() < window.FELOG_SAMPLING_API || w.felog && window.FELOG_ENABLE_APIS.indexOf(w.felog) > -1;
            ("requestSuccess" != e || m) && this.send({
                t1: "monitor",
                t2: "api",
                t3: e,
                d1: t.replace(/^(https?:)?/, ""),
                d2: r + "-" + a + "-" + w.felog,
                d3: f + "-" + d,
                d4: o(l),
                d5: o(JSON.stringify(w))
            })
        }
    }
    ,
    FELOG.requestSuccess = function(t, e, n) {
        this.request(t, "requestSuccess", e, n)
    }
    ,
    FELOG.requestError = FELOG.requestReject = FELOG.requestCrash = function(t, e, n) {
        this.request(t, "requestError", e, n)
    }
    ;
    var S = {
        parseResponse: function(t, e) {
            var n = t;
            if ("string" == typeof n)
                try {
                    n = JSON.parse(t)
                } catch (t) {}
            return "object" != typeof n ? {} : {
                msg: n.message,
                code: n.code,
                success: _(n, e),
                body: n.body
            }
        },
        isSuccess: _,
        getResponseBody: function(t, e) {
            if (e.originResponse)
                return t;
            if ("jsonp" === e.method)
                return t.json();
            var n = e.headers && e.headers.accept || "text"
              , o = t.headers && t.headers.get ? t.headers.get("content-type") : null;
            return o || (o = n),
            -1 !== o.toLowerCase().indexOf("application/json") ? t.json() : -1 !== o.toLowerCase().indexOf("text") ? t.text() : t.blob()
        }
    };
    function b(t, e, n, o, i) {
        var r = n > window.FELOG_MAX_API_LATENCY || Math.random() < window.FELOG_SAMPLING_API;
        t.success && !r || FELOG[t.success ? "requestSuccess" : "requestError"](e, {
            status: o,
            duration: n,
            traceId: i,
            code: t.code,
            msg: t.msg,
            body: t.body,
            type: "xhr"
        })
    }
    FELOG.injectFetchHook = function() {
        if ("function" == typeof window.fetch) {
            var t = window.fetch
              , e = function(t, e, n, o, i) {
                var r = o;
                t ? t.text().then((function(t) {
                    if (t)
                        try {
                            r = JSON.parse(t)
                        } catch (e) {
                            r = t
                        }
                    FELOG[i](e, g({}, n, {
                        params: r
                    }))
                }
                )).catch((function() {}
                )) : FELOG[i](e, g({}, n, {
                    params: r
                }))
            };
            window.fetch = function(n, o) {
                var i = 1 === arguments.length ? [arguments[0]] : Array.apply(null, arguments);
                if (o && ("HEAD" === o.method || "no-cors" === o.mode))
                    return t.apply(window, i);
                var r = (n && "string" != typeof n ? n.url : n) || "";
                if (r.match(/\.(js|css|png|jpg|gif|jpeg|webp)(\?.*)?$/))
                    return t.apply(window, i);
                var s = Date.now()
                  , a = "";
                return i[0]instanceof Request && (a = i[0].clone()),
                t.apply(window, i).then((function(t) {
                    var n = t.clone ? t.clone() : t;
                    return S.getResponseBody(n, o || {}).then((function(t) {
                        var o = Date.now() - s
                          , c = {};
                        t && "object" == typeof t && (c = t);
                        var d = n.status;
                        c = S.parseResponse(c, d);
                        var u = "";
                        try {
                            u = n.headers.get("traceid")
                        } catch (t) {}
                        var f = c.success ? "requestSuccess" : "requestError"
                          , h = {
                            status: d,
                            duration: o,
                            traceId: u,
                            code: c.code,
                            msg: c.msg,
                            body: c.body,
                            type: "fetch"
                        };
                        e(a, r, h, i, f)
                    }
                    )).catch((function() {}
                    )),
                    t
                }
                ), (function(t) {
                    var n = {
                        status: 401,
                        duration: Date.now() - s,
                        msg: t.stack || t.message,
                        type: "fetch"
                    };
                    return e(a, r, n, i, "requestError"),
                    console.error(t),
                    t
                }
                ))
            }
        }
    }
    ,
    FELOG.injectXhrHook = function() {
        if ("function" == typeof window.XMLHttpRequest && window.addEventListener) {
            var t = window.XMLHttpRequest;
            window.XMLHttpRequest = function(e) {
                var n, o, i, r = new t(e), s = r.send, a = r.open;
                return r.open = function(t, e) {
                    var n = 1 === arguments.length ? [arguments[0]] : Array.apply(null, arguments);
                    a.apply(r, n),
                    (o = e || "").match("logstores") && (i = !0)
                }
                ,
                r.send = function(t) {
                    n = Date.now(),
                    s.apply(r, arguments)
                }
                ,
                r.addEventListener("readystatechange", (function(t) {
                    if (!i && o && 4 === r.readyState) {
                        var e, s = Date.now() - n, a = r.status;
                        try {
                            -1 !== r.getAllResponseHeaders().indexOf("traceid") && (e = r.getResponseHeader("traceid"))
                        } catch (t) {}
                        if (r.responseType && "text" !== r.responseType) {
                            if ("blob" === r.responseType) {
                                var c = new FileReader;
                                c.readAsText.apply(c, [r.response]),
                                c.onloadend = function() {
                                    b(S.parseResponse(c.result, a), o, s, a, e)
                                }
                            }
                        } else
                            b(S.parseResponse(r.responseText, a), o, s, a, e)
                    }
                }
                )),
                r
            }
        }
    }
    ,
    FELOG.PV = function(t, e) {
        function n() {
            var t = 0
              , e = 0
              , n = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
            return n && (t = n.rtt || 0,
            e = n.effectiveType || ""),
            [e, t]
        }
        var o = performance.memory || {}
          , i = o.jsHeapSizeLimit
          , r = void 0 === i ? 0 : i
          , s = o.totalJSHeapSize
          , a = void 0 === s ? 0 : s
          , c = o.usedJSHeapSize
          , d = void 0 === c ? 0 : c;
        this.send({
            t1: "bu",
            t2: "pv",
            d1: navigator.platform + "," + navigator.hardwareConcurrency + "," + r + "," + a + "," + d,
            d2: n()[1],
            d3: window.screen.width + "x" + window.screen.height,
            d4: window.innerWidth + "x" + window.innerHeight,
            d5: navigator.userAgent.replace(/ /g, "")
        });
        var u = window.history.pushState
          , f = window.history.replaceState;
        window.history.pushState = function(t, e, o) {
            FELOG.send({
                t1: "bu",
                t2: "pv",
                t3: "spa",
                d1: n()[0],
                d2: n()[1],
                d5: JSON.stringify(t)
            }),
            u.apply(window.history, arguments)
        }
        ,
        window.history.replaceState = function(t, e, o) {
            FELOG.send({
                t1: "bu",
                t2: "pv",
                t3: "spa",
                d1: n()[0],
                d2: n()[1],
                d5: JSON.stringify(t)
            }),
            f.apply(window.history, arguments)
        }
    }
    ,
    FELOG.custom = function(t, e) {
        Object.keys(t).length && this.send({
            t1: "bu",
            t2: "custom",
            t3: o(t.t3),
            d1: o(t.d1),
            d2: o(t.d2),
            d3: o(t.d3),
            d4: o(t.d4),
            d5: o(t.d5)
        }, !!e)
    }
    ;
    FELOG.FMP = function() {
        var t = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver;
        if (t) {
            var e, n = 0, o = Date.now(), i = new t((function(t) {
                var e = t.length;
                n > 0 && e / n > 4 && (window.FELOG_FMP = Date.now() - o,
                i.disconnect()),
                n = e
            }
            ));
            e = function() {
                var t = document.querySelector("#ice-container") || document.body;
                i.observe(t, {
                    attributes: !0,
                    childList: !0,
                    characterData: !0,
                    subtree: !0
                })
            }
            ,
            "interactive" === document.readyState ? e() : document.addEventListener("DOMContentLoaded", e),
            setTimeout((function() {
                i.disconnect()
            }
            ), 8e3)
        }
    }
    ,
    FELOG.timing = function() {
        if (this.navigationStart) {
            e((function t() {
                var e = setTimeout((function() {
                    var n = performance.timing
                      , o = n.fetchStart
                      , i = n.connectStart
                      , r = n.requestStart
                      , s = n.responseEnd
                      , a = n.responseStart
                      , c = n.loadEventStart
                      , d = n.domLoading
                      , u = n.domContentLoadedEventStart;
                    u ? (FELOG.send({
                        t1: "exp",
                        t2: "timing",
                        t3: r - i,
                        d1: a - r,
                        d2: s - a,
                        d3: u - d,
                        d4: c - u,
                        d5: i - o
                    }),
                    clearTimeout(e)) : (clearTimeout(e),
                    t())
                }
                ), 3e3)
            }
            ))
        }
    }
    ,
    FELOG.fp = function() {
        var o = 0;
        if (window.PerformanceElementTiming) {
            var i = new PerformanceObserver((function(t) {
                var e = t.getEntries();
                o = e[0],
                i.disconnect()
            }
            ));
            i.observe({
                entryTypes: ["element"]
            }),
            p((function(e) {
                e ? t((function() {
                    i.observe({
                        entryTypes: ["element"]
                    })
                }
                ), 50) : i.disconnect()
            }
            ))
        }
        if (this.navigationStart) {
            e((function t() {
                var e = setTimeout((function() {
                    var i = performance.getEntriesByName("first-paint")[0]
                      , r = performance.getEntriesByName("first-contentful-paint")[0];
                    if (window.FELOG_TTI) {
                        var s = n(r && r.startTime)
                          , a = o ? n(o.startTime) : window.FELOG_FMP || 0
                          , c = n(window.FELOG_TTI > s ? window.FELOG_TTI : s) || s
                          , d = n(window.FELOG_TBT);
                        FELOG.send({
                            t1: "exp",
                            t2: "fp",
                            t3: location.pathname.split("/")[1],
                            d1: n(i && i.startTime),
                            d2: s,
                            d3: a,
                            d4: c,
                            d5: d
                        }),
                        clearTimeout(e)
                    } else
                        t()
                }
                ), 3e3)
            }
            ))
        }
    }
    ,
    FELOG.fid = function() {
        try {
            var t = new PerformanceObserver((function(e, o) {
                var i = e.getEntries()[0];
                if (i) {
                    var r = i.processingStart - i.startTime
                      , s = i.duration;
                    (r > 50 || s > 50) && FELOG.send({
                        t1: "bu",
                        t2: "custom",
                        t3: "fid",
                        d1: r ? n(r) : 0,
                        d2: s ? n(s) : 0
                    })
                }
                t.disconnect()
            }
            ));
            t.observe({
                entryTypes: ["first-input"]
            }),
            p((function(e) {
                !e && t && t.disconnect()
            }
            ))
        } catch (t) {}
    }
    ,
    FELOG.lcp = function() {
        try {
            var t = new PerformanceObserver((function(t) {
                t.getEntries().forEach((function(t) {
                    FELOG.send({
                        t1: "exp",
                        t2: "fe",
                        t3: "lcp",
                        d1: n(t.startTime),
                        d2: t.size,
                        d3: E(t.element)
                    })
                }
                ))
            }
            ));
            t.observe({
                entryTypes: ["largest-contentful-paint"]
            }),
            e((function() {
                t && t.disconnect()
            }
            )),
            p((function(e) {
                !e && t && t.disconnect()
            }
            ))
        } catch (t) {}
    }
    ,
    FELOG.cls = function() {
        try {
            var e = new PerformanceObserver((function(t) {
                t.getEntries().forEach((function(t) {
                    if (t.sources && t.value > .1) {
                        var e = t.sources[0] ? E(t.sources[0].node) : ""
                          , n = t.sources[1] ? E(t.sources[1].node) : ""
                          , o = t.sources[2] ? E(t.sources[2].node) : "";
                        FELOG.send({
                            t1: "exp",
                            t2: "fe",
                            t3: "cls",
                            d1: t.startTime,
                            d2: t.value,
                            d3: e,
                            d4: n,
                            d5: o
                        })
                    }
                }
                ))
            }
            ));
            e.observe({
                entryTypes: ["layout-shift"]
            }),
            p((function(n) {
                !n && e ? e.disconnect() : t((function() {
                    e.observe({
                        entryTypes: ["layout-shift"]
                    })
                }
                ), 50)
            }
            ))
        } catch (t) {}
    }
    ;
    FELOG.longTask = function() {
        if (window.PerformanceLongTaskTiming) {
            FELOG._lastLongtaskSelList = [],
            window.FELOG_TBT = 0;
            var e, o = performance.now(), i = new PerformanceObserver((function(r) {
                r.getEntries().forEach((function(i) {
                    if (o = performance.now(),
                    clearTimeout(e),
                    e = setTimeout((function() {
                        window.FELOG_TTI = o,
                        i.duration > 50 && (window.FELOG_TBT += i.duration - 50)
                    }
                    ), 3e3),
                    i.duration > 500 && FELOG._lastLongtaskSelList.length < 100) {
                        var r = y();
                        t((function() {
                            var t = r ? E(r.path || r.target) : "";
                            FELOG._lastLongtaskSelList.indexOf(t) < 0 && (FELOG.send({
                                t1: "exp",
                                t2: "longtask",
                                d1: n(i.startTime),
                                d2: n(i.duration),
                                d3: t
                            }),
                            FELOG._lastLongtaskSelList.push(t))
                        }
                        ))
                    }
                }
                )),
                FELOG._lastLongtaskSelList.length >= 100 && i.disconnect()
            }
            ));
            setTimeout((function() {
                window.FELOG_TTI = o
            }
            ), 21e3),
            i.observe({
                entryTypes: ["longtask"]
            }),
            p((function(e) {
                e ? t((function() {
                    i.observe({
                        entryTypes: ["longtask"]
                    })
                }
                ), 50) : i.disconnect()
            }
            ))
        }
    }
    ,
    FELOG.eventTiming = function() {
        if (window.PerformanceEventTiming) {
            var e = new PerformanceObserver((function(e) {
                var o = e.getEntries().filter((function(t) {
                    return t.processingEnd - t.processingStart > 1
                }
                )).sort((function(t, e) {
                    return e.processingEnd - e.processingStart - (t.processingEnd - t.processingStart)
                }
                ))[0];
                if (o) {
                    var i = y();
                    t((function() {
                        FELOG.send({
                            t1: "exp",
                            t2: "eventTiming",
                            t3: o.name,
                            d1: n(o.startTime),
                            d2: n(o.duration),
                            d3: i ? E(i.path || i.target) : "",
                            d4: n(o.processingEnd - o.processingStart)
                        })
                    }
                    ))
                }
            }
            ));
            e.observe({
                entryTypes: ["event"]
            }),
            p((function(n) {
                n ? t((function() {
                    e.observe({
                        entryTypes: ["event"]
                    })
                }
                ), 50) : e.disconnect()
            }
            ))
        }
    }
    ;
    FELOG.entries = function() {
        var t = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {};
        e((function() {
            setTimeout((function() {
                var e = window.performance;
                if (e.getEntries) {
                    var o = e.getEntries(t);
                    o.length && o.forEach((function(t) {
                        var e = t.name
                          , o = t.duration
                          , i = t.transferSize
                          , r = t.decodedBodySize
                          , s = t.requestStart
                          , a = t.connectStart
                          , c = t.responseStart
                          , d = t.responseEnd
                          , u = t.fetchStart;
                        (e.endsWith(".js") || e.endsWith(".css")) && (i > 3e5 || o > 200) && window.FELOG_ENABLE_ENTRY && FELOG.send({
                            t1: "exp",
                            t2: "entries",
                            t3: e,
                            d1: i + "-" + r,
                            d2: n(a - u),
                            d3: n(s - a),
                            d4: n(c - s),
                            d5: n(d - c)
                        })
                    }
                    ))
                }
            }
            ), 3e3)
        }
        ))
    }
    ,
    function() {
        function t(t) {
            return t ? ((t = t.split("\n").slice(1)).length > G && (t = t.slice(0, 2).concat(["...", t[t.length - 1]])),
            t.map((function(t) {
                return t.replace(/^\s+at\s+/g, "")
            }
            )).join("^")) : ""
        }
        window.addEventListener("error", (function(e, i, r, s, a) {
            var c = y();
            try {
                "string" == typeof e ? FELOG.send({
                    t1: "monitor",
                    t2: "jserror",
                    d1: e || "",
                    d2: o(i),
                    d3: ":" + (r || 0) + ":" + (s || 0),
                    d4: t(a && a.stack),
                    d5: c ? E(c.path || c.target) : ""
                }) : e.target && (e.target.src || e.target.href) ? FELOG.send({
                    t1: "monitor",
                    t2: "res",
                    t3: e.target.src || e.target.href,
                    d1: e.target.tagName,
                    d2: n(e.timeStamp),
                    d3: E(e.path || e.target)
                }) : FELOG.send({
                    t1: "monitor",
                    t2: "jserror",
                    d1: e.message || "",
                    d2: o(e.filename),
                    d3: ":" + (e.lineno || 0) + ":" + (e.colno || 0),
                    d4: t(e.error && e.error.stack),
                    d5: c ? E(c.path || c.target) : ""
                })
            } catch (e) {}
        }
        ), !0),
        window.addEventListener("unhandledrejection", (function(e) {
            if (e) {
                var n = y();
                try {
                    var i = ""
                      , r = 0
                      , s = 0
                      , a = ""
                      , c = "";
                    "string" == typeof e ? i = e : "object" == typeof e.reason ? i = e.reason.message : "string" == typeof e.message && (i = e.message);
                    var d = e.reason;
                    if ("object" == typeof d) {
                        if ("number" == typeof d.column)
                            s = d.column,
                            r = d.line;
                        else if (d.stack) {
                            (u = d.stack.match(/at\s+.+:(\d+):(\d+)/)) && (r = u[1],
                            s = u[2])
                        }
                        if (d.sourceURL)
                            a = d.sourceURL;
                        else if (d.stack) {
                            var u;
                            (u = d.stack.match(/at\s+(.+):\d+:\d+/)) && (a = u[1])
                        }
                        d.stack && (c = t(d.stack))
                    }
                    FELOG.send({
                        t1: "monitor",
                        t2: "jserror",
                        t3: "promise",
                        d1: i || "",
                        d2: o(a),
                        d3: ":" + r + ":" + s,
                        d4: c,
                        d5: n ? E(n.path || n.target) : ""
                    })
                } catch (e) {}
            }
        }
        ))
    }(),
    window.FELOG_DISABLE_API_INJECT || (window.FELOG_ENABLE_APIS = [],
    window.FELOG_MAX_API_LATENCY = window.FELOG_MAX_API_LATENCY || 800,
    window.FELOG_SAMPLING_API = window.FELOG_SAMPLING_API || .01,
    FELOG.injectFetchHook(),
    FELOG.injectXhrHook()),
    navigator.serviceWorker && navigator.serviceWorker.addEventListener("message", (function(t) {
        if (console.log("sw message", t.data),
        "felog" === t.data.type)
            try {
                FELOG.send(JSON.parse(t.data.msg))
            } catch (t) {
                console.log(t)
            }
    }
    )),
    FELOG.FMP(),
    FELOG.PV(),
    FELOG.entries(),
    window.FELOG_SAMPLING = window.FELOG_SAMPLING || .01,
    "PerformanceObserver"in window && ["longTask", "eventTiming", "timing", "fp", "fid", "lcp", "cls"].forEach((function(t) {
        var e = 1;
        void 0 !== window["FELOG_SAMPLING_" + t] ? e = window["FELOG_SAMPLING_" + t] : void 0 !== window.FELOG_SAMPLING && (e = FELOG_SAMPLING),
        Math.random() < e && FELOG[t]()
    }
    ))
}();
