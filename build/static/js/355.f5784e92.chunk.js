"use strict";(self.webpackChunkconference=self.webpackChunkconference||[]).push([[355,227,381,814],{4609:function(e,n,s){s.r(n),s.d(n,{default:function(){return v}});var c=s(3433),l=s(9439),r=s(2791),a=s(7689),i=s(3708),d=s(9916),t=s(9434);var o=s.p+"static/media/followSmall.79c19ee94ee0dedd1c8d97cdcb63fc4f.svg";var f=s.p+"static/media/followingSmall.4562cb8f2f92096467031c2988cdada8.svg",h=s(3105),_=s(8131),u=s(7646),x=s(8703),j=s.n(x),g=s(184),v=function(){var e,n=(0,a.UO)().confId,s=(0,t.v9)((function(e){return e.conferences})).conferences,x=JSON.parse(window.localStorage.getItem("fave"))||[],v=(0,r.useState)(x),m=(0,l.Z)(v,2),b=m[0],p=m[1],N=(0,t.I0)(),w=(0,r.useState)(!0),k=(0,l.Z)(w,2),S=k[0],D=k[1],C=(0,r.useState)(!1),L=(0,l.Z)(C,2),Y=L[0],Z=L[1],y=s.find((function(e){return e.id===+n}));return 0===s.length&&(e=(0,g.jsx)(h.ZP,{})),s.filter((function(e){return e.id===+n})).length>0?e=(0,g.jsxs)("div",{className:"full-conference__container",children:[(0,g.jsxs)("div",{className:"full-conference__container-top",children:[!1===y.register&&!1===y.finished&&(0,g.jsx)("span",{style:{backgroundColor:"#939393"},children:"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u0437\u0430\u043a\u043e\u043d\u0447\u0435\u043d\u0430"})||!1===y.register&&!0===y.finished&&(0,g.jsx)("span",{style:{backgroundColor:"#939393"},children:"\u041a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u044f \u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0430"})||!0===y.register&&!1===y.finished&&(0,g.jsx)("span",{children:"\u0418\u0434\u0435\u0442 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f"}),(0,g.jsx)("img",{title:!1===y.follow?"\u0434\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432 \u0438\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435":"\u0443\u0434\u0430\u043b\u0438\u0442\u044c \u0438\u0437 \u0438\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0433\u043e",src:!1===y.follow?o:f,alt:"follow",onClick:function(){var e;e=y.id,b.includes(e)?(p(b.filter((function(n){return n!==e}))),console.log(b)):p([].concat((0,c.Z)(b),[e])),N((0,d.xe)(y.id))},width:"32",height:"32"})]}),(0,g.jsxs)("div",{className:"full-conference__title",children:[(0,g.jsx)("h1",{children:y.conf_name}),(0,g.jsxs)("small",{children:["\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430 \u043d\u0430 ",y.conf_date_begin," "]})]}),(0,g.jsxs)("div",{className:"full-conference__card",children:[(0,g.jsxs)("div",{className:"full-conference__card-flex",children:[(0,g.jsxs)("div",{children:[(0,g.jsx)("span",{children:"\u0414\u0430\u0442\u0430 \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u044f:"}),null===y.conf_date_end&&null===y.conf_date_begin?"\u0434\u0430\u0442\u0430 \u0443\u0442\u043e\u0447\u043d\u044f\u0435\u0442\u0441\u044f":null!==y.conf_date_end?new Date(y.conf_date_begin).toLocaleDateString("ru",_.Y).slice(0,-3)+" - "+new Date(y.conf_date_end).toLocaleDateString("ru",_.Y).slice(0,-3):new Date(y.conf_date_begin).toLocaleDateString("ru",_.Y).slice(0,-3)]}),(0,g.jsxs)("div",{children:[(0,g.jsx)("span",{children:"\u0424\u043e\u0440\u043c\u0430 \u0443\u0447\u0430\u0441\u0442\u0438\u044f:"}),(0,g.jsxs)("span",{className:"both",children:[y.online?"\u043e\u043d\u043b\u0430\u0439\u043d":""," ",y.offline?"\u043e\u0444\u0444\u043b\u0430\u0439\u043d":""]})]}),(0,g.jsxs)("div",{children:[(0,g.jsx)("span",{children:"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f:"}),null===y.reg_date_begin&&null===y.reg_date_end&&(0,g.jsx)("span",{className:"online",children:"\u0434\u0430\u0442\u0430 \u0443\u0442\u043e\u0447\u043d\u044f\u0435\u0442\u0441\u044f"}),null===y.reg_date_begin&&null!==y.reg_date_end&&(0,g.jsxs)("span",{className:"online",children:[" ","\u0434\u043e"," ",new Date(y.reg_date_end).toLocaleDateString("ru",_.Y).slice(0,-3)," "]})||null!==y.reg_date_begin&&null!==y.reg_date_end&&(0,g.jsxs)("span",{className:"online",children:[" ",new Date(y.reg_date_begin).toLocaleDateString("ru",_.Y).slice(0,-3),"-",new Date(y.reg_date_end).toLocaleDateString("ru",_.Y).slice(0,-3)]})]}),(0,g.jsxs)("div",{children:[(0,g.jsx)("span",{children:"\u041f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u044f:"}),(0,g.jsx)("span",{className:"online",children:y.rinc?"\u0440\u0438\u043d\u0446":"\u0431\u0435\u0437 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438"})]})]}),(0,g.jsx)("hr",{}),(0,g.jsxs)("div",{className:"full-conference__card-block",children:[(0,g.jsxs)("div",{children:[(0,g.jsx)("span",{children:"\u041e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0442\u043e\u0440:"})," ",y.org_name]}),(0,g.jsx)("hr",{}),(0,g.jsxs)("div",{children:[(0,g.jsx)("span",{children:"\u0422\u0435\u043c\u0430\u0442\u0438\u043a\u0430:"})," ",(0,g.jsxs)("span",{className:"online",children:[" ",y.themes]})]})]})]}),(0,g.jsxs)("div",{className:"full-conference__tabs",children:[(0,g.jsx)("button",{className:S?"button-active":"button-passive",onClick:function(){!0===Y&&(Z(!1),D(!0))},children:"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435"}),(0,g.jsx)("button",{className:Y?"button-active":"button-passive",onClick:function(){!0===S&&D(!1),Z(!0)},children:"\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u044b"})]}),S&&!Y&&(0,g.jsxs)("div",{className:"full-conference__desc",children:[(0,g.jsx)("h1",{children:"\u0423\u0441\u043b\u043e\u0432\u0438\u044f \u0443\u0447\u0430\u0441\u0442\u0438\u044f"}),0===y.conf_desc.length&&(0,g.jsx)("a",{href:y.conf_card_href,rel:"noreferrer",target:"_blank",children:"\u041f\u043e\u0434\u0440\u043e\u0431\u043d\u0435\u0435 \u043e \u043a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438"})||y.conf_card_href.length>0&&(0,g.jsxs)("pre",{children:[(0,g.jsx)("div",{className:"full-conference__desc-parsed",dangerouslySetInnerHTML:{__html:j().sanitize(y.conf_desc)}}),(0,g.jsx)("div",{children:(0,g.jsx)("a",{href:y.conf_card_href,rel:"noreferrer",target:"_blank",children:"\u041f\u043e\u0434\u0440\u043e\u0431\u043d\u0435\u0435 \u043e \u043a\u043e\u043d\u0444\u0435\u0440\u0435\u043d\u0446\u0438\u0438"})})]})]}),!S&&Y&&(0,g.jsxs)("div",{className:"full-conference__contacts",children:[(0,g.jsxs)("div",{children:[(0,g.jsx)("span",{children:"\u0410\u0434\u0440\u0435\u0441 "}),(0,g.jsx)("br",{})," ",y.conf_address]}),(0,g.jsxs)("div",{children:[(0,g.jsx)("span",{children:"\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u0430\u044f \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f "}),(0,g.jsx)("br",{})," ",(0,g.jsx)("span",{className:"details",children:y.contacts})]}),(0,g.jsxs)("div",{children:[(0,g.jsx)("span",{children:"\u041f\u043e\u043b\u0435\u0437\u043d\u044b\u0435 \u0441\u0441\u044b\u043b\u043a\u0438 "}),(0,g.jsx)("br",{}),y.conf_card_href.length>0&&(0,g.jsx)("a",{rel:"noreferrer",target:"_blank",href:y.conf_card_href,children:"\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a"}),(0,g.jsx)("br",{}),y.reg_href.length>0&&(0,g.jsx)("a",{rel:"noreferrer",target:"_blank",href:y.reg_href,children:"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f"})]})]})]}):s.length&&!y&&(e=(0,g.jsx)(i.default,{})),(0,r.useEffect)((function(){N((0,d.N0)()),window.scrollTo(0,0),N((0,d.c3)(b))}),[n,N,b]),(0,g.jsxs)(g.Fragment,{children:[(0,g.jsx)("div",{className:"full-conference",children:e}),y&&(0,g.jsx)("div",{children:(0,g.jsx)(u.default,{data:"prev4",keywords:y.themes,id:y.id})})]})}}}]);
//# sourceMappingURL=355.f5784e92.chunk.js.map