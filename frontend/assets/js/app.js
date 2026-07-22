const CONFIG = {
  MOCK_MODE: true,
  API_BASE_URL: "/api",
  ENDPOINTS: {
    register: "/auth/register",
    login: "/auth/login",
    upload: "/upload",
    gallery: "/gallery",
    standardEdit: "/edit/standard",
    aiEdit: "/edit/ai"
  }
};

const state = {
  user: JSON.parse(localStorage.getItem("neuropix_user") || "null"),
  gallery: JSON.parse(localStorage.getItem("neuropix_gallery") || "[]"),
  image: null,
  originalUrl: "",
  modifiedUrl: "",
  fileName: "",
  editType: "standard",
  selectedAiTool: "upscale",
  rotation: 0,
  flipH: 1,
  flipV: 1,
  brightness: 100,
  contrast: 100,
  saturation: 100
};

const $ = (s, c=document) => c.querySelector(s);
const $$ = (s, c=document) => [...c.querySelectorAll(s)];
const showToast = (message) => {
  const toast = $("#toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast.t);
  showToast.t = setTimeout(() => toast.classList.remove("show"), 2600);
};

function route(name) {
  $$(".view").forEach(v => v.classList.remove("active"));
  if (name === "landing") $("#landingView").classList.add("active");
  if (name === "login" || name === "register") {
    $("#authView").classList.add("active");
    setAuthMode(name);
  }
  if (name === "app") {
    if (!state.user) return route("login");
    $("#appView").classList.add("active");
    updateUserUI();
    updateDashboard();
    renderGallery();
  }
  window.scrollTo({top:0, behavior:"smooth"});
}

function setAuthMode(mode) {
  $("#loginForm").classList.toggle("hidden", mode !== "login");
  $("#registerForm").classList.toggle("hidden", mode !== "register");
}

$$("[data-route]").forEach(el => el.addEventListener("click", e => {
  e.preventDefault(); route(el.dataset.route);
}));
$$("[data-auth-mode]").forEach(el => el.addEventListener("click", () => setAuthMode(el.dataset.authMode)));
$$(".show-pass").forEach(btn => btn.addEventListener("click", () => {
  const input = document.getElementById(btn.dataset.target);
  input.type = input.type === "password" ? "text" : "password";
  btn.textContent = input.type === "password" ? "Show" : "Hide";
}));

$("#registerPassword").addEventListener("input", e => {
  const value = e.target.value;
  let score = 0;
  if (value.length >= 8) score++;
  if (/[A-Z]/.test(value)) score++;
  if (/[0-9]/.test(value)) score++;
  if (/[^A-Za-z0-9]/.test(value)) score++;
  const bar = $("#strengthBar");
  bar.style.width = `${score * 25}%`;
  bar.style.background = score < 2 ? "#d64545" : score < 4 ? "#e0a72d" : "#16a36a";
});

$("#loginForm").addEventListener("submit", async e => {
  e.preventDefault();
  const username = $("#loginUsername").value.trim();
  const password = $("#loginPassword").value;
  if (CONFIG.MOCK_MODE) {
    state.user = {username, email:`${username.toLowerCase().replace(/\s+/g,".")}@example.com`};
    localStorage.setItem("neuropix_user", JSON.stringify(state.user));
    route("app");
    showToast("Logged in successfully.");
    return;
  }
  const res = await fetch(CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.login, {
    method:"POST", headers:{"Content-Type":"application/json"},
    body:JSON.stringify({username,password})
  });
  if (!res.ok) return showToast("Login failed.");
  state.user = await res.json();
  localStorage.setItem("neuropix_user", JSON.stringify(state.user));
  route("app");
});

$("#registerForm").addEventListener("submit", async e => {
  e.preventDefault();
  const username = $("#registerUsername").value.trim();
  const email = $("#registerEmail").value.trim();
  const password = $("#registerPassword").value;
  if (password !== $("#confirmPassword").value) return showToast("Passwords do not match.");
  if (CONFIG.MOCK_MODE) {
    state.user = {username,email};
    localStorage.setItem("neuropix_user", JSON.stringify(state.user));
    route("app");
    showToast("Account created in frontend demo mode.");
    return;
  }
  const res = await fetch(CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.register, {
    method:"POST", headers:{"Content-Type":"application/json"},
    body:JSON.stringify({username,password,email})
  });
  if (!res.ok) return showToast("Registration failed.");
  setAuthMode("login");
});

const pageMeta = {
  dashboard:["Overview","Dashboard"],
  editor:["Create","Image editor"],
  gallery:["Library","My gallery"],
  profile:["Account","Profile"],
  settings:["Preferences","Settings"]
};

function openAppPage(page) {
  $$(".app-page").forEach(p => p.classList.remove("active"));
  $(`#${page}Page`).classList.add("active");
  $$(".side-nav button").forEach(b => b.classList.toggle("active", b.dataset.appPage === page));
  $("#pageEyebrow").textContent = pageMeta[page][0];
  $("#pageTitle").textContent = pageMeta[page][1];
  $("#sidebar").classList.remove("open");
}
$$("[data-app-page]").forEach(el => el.addEventListener("click", () => openAppPage(el.dataset.appPage)));
$$("[data-tool-start]").forEach(el => el.addEventListener("click", () => {
  openAppPage("editor");
  if (el.dataset.toolStart !== "standard") {
    $('[data-tool-tab="ai"]').click();
    $(`[data-ai-tool="${el.dataset.toolStart}"]`)?.click();
  }
}));

$("#sidebarToggle").addEventListener("click", () => $("#sidebar").classList.toggle("open"));
$("#logoutBtn").addEventListener("click", () => {
  state.user = null;
  localStorage.removeItem("neuropix_user");
  route("landing");
  showToast("Logged out.");
});

function updateUserUI() {
  const username = state.user?.username || "User";
  const email = state.user?.email || "user@example.com";
  const initial = username.charAt(0).toUpperCase();
  ["topUsername","welcomeUsername","profileUsername"].forEach(id => document.getElementById(id).textContent = username);
  ["avatarInitial","profileAvatar"].forEach(id => document.getElementById(id).textContent = initial);
  $("#profileEmail").textContent = email;
  $("#profileUsernameInput").value = username;
  $("#profileEmailInput").value = email;
}

$("#profileForm").addEventListener("submit", e => {
  e.preventDefault();
  state.user.username = $("#profileUsernameInput").value.trim();
  state.user.email = $("#profileEmailInput").value.trim();
  localStorage.setItem("neuropix_user", JSON.stringify(state.user));
  updateUserUI();
  showToast("Profile updated.");
});

function updateDashboard() {
  const total = state.gallery.length;
  const ai = state.gallery.filter(i => i.editType === "ai").length;
  const standard = total - ai;
  $("#totalImages").textContent = total;
  $("#aiEdits").textContent = ai;
  $("#standardEdits").textContent = standard;
  $("#latestUpload").textContent = total ? new Date(state.gallery[0].date).toLocaleDateString(undefined,{month:"short",day:"numeric"}) : "—";
  $("#storageText").textContent = `${total} / 50 images`;
  $("#storageBar").style.width = `${Math.min(total/50*100,100)}%`;
  const recent = $("#recentList");
  if (!total) {
    recent.className = "recent-list empty-state small";
    recent.innerHTML = "<span>▧</span><p>No images processed yet.</p>";
  } else {
    recent.className = "recent-list";
    recent.innerHTML = state.gallery.slice(0,3).map(item => `
      <div class="recent-item"><img src="${item.modifiedUrl}" alt=""><div><strong>${escapeHtml(item.name)}</strong><small>${item.editType.toUpperCase()} • ${new Date(item.date).toLocaleDateString()}</small></div></div>
    `).join("");
  }
}

const uploadZone = $("#uploadZone");
$("#chooseFileBtn").addEventListener("click", () => $("#fileInput").click());
$("#replaceImageBtn").addEventListener("click", () => $("#fileInput").click());
$("#fileInput").addEventListener("change", e => handleFile(e.target.files[0]));
["dragenter","dragover"].forEach(type => uploadZone.addEventListener(type, e => {e.preventDefault(); uploadZone.classList.add("dragover")}));
["dragleave","drop"].forEach(type => uploadZone.addEventListener(type, e => {e.preventDefault(); uploadZone.classList.remove("dragover")}));
uploadZone.addEventListener("drop", e => handleFile(e.dataTransfer.files[0]));

function handleFile(file) {
  if (!file) return;
  if (!["image/jpeg","image/png"].includes(file.type)) return showToast("Only JPG and PNG files are allowed.");
  const url = URL.createObjectURL(file);
  const img = new Image();
  img.onload = () => {
    if (img.width > 1920 || img.height > 1080) {
      URL.revokeObjectURL(url);
      return showToast(`Image is ${img.width}×${img.height}. Maximum is 1920×1080.`);
    }
    state.image = file;
    state.originalUrl = url;
    state.modifiedUrl = url;
    state.fileName = file.name;
    resetTransforms();
    $("#originalImage").src = url;
    $("#modifiedImage").src = url;
    $("#uploadZone").classList.add("hidden");
    $("#workspace").classList.remove("hidden");
    $("#editorStatus").textContent = `${img.width} × ${img.height}`;
    $("#editorStatus").classList.add("success");
    showToast("Image validated and loaded.");
  };
  img.src = url;
}

function resetTransforms() {
  state.rotation=0; state.flipH=1; state.flipV=1; state.brightness=100; state.contrast=100; state.saturation=100;
  $("#brightnessRange").value=100; $("#contrastRange").value=100; $("#saturationRange").value=100;
  updateRangeLabels(); applyPreviewFilter();
}
function updateRangeLabels() {
  $("#brightnessValue").textContent = `${state.brightness}%`;
  $("#contrastValue").textContent = `${state.contrast}%`;
  $("#saturationValue").textContent = `${state.saturation}%`;
}
function applyPreviewFilter() {
  $("#modifiedImage").style.filter = `brightness(${state.brightness}%) contrast(${state.contrast}%) saturate(${state.saturation}%)`;
  $("#modifiedImage").style.transform = `rotate(${state.rotation}deg) scale(${state.flipH},${state.flipV})`;
}
[["brightnessRange","brightness"],["contrastRange","contrast"],["saturationRange","saturation"]].forEach(([id,key]) => {
  $(`#${id}`).addEventListener("input", e => {state[key]=Number(e.target.value); updateRangeLabels(); applyPreviewFilter();});
});
$$("[data-standard-tool]").forEach(btn => btn.addEventListener("click", () => {
  if (!state.image) return showToast("Choose an image first.");
  const tool = btn.dataset.standardTool;
  if (tool==="flip_h") state.flipH *= -1;
  if (tool==="flip_v") state.flipV *= -1;
  if (tool==="rotate") state.rotation = (state.rotation + 90) % 360;
  applyPreviewFilter();
}));

$("#compareRange").addEventListener("input", e => {
  const v = e.target.value;
  $("#afterLayer").style.width = `${v}%`;
  $("#sliderLine").style.left = `${v}%`;
});

$$("[data-tool-tab]").forEach(btn => btn.addEventListener("click", () => {
  $$("[data-tool-tab]").forEach(b => b.classList.toggle("active", b===btn));
  $("#standardTools").classList.toggle("hidden", btn.dataset.toolTab !== "standard");
  $("#aiTools").classList.toggle("hidden", btn.dataset.toolTab !== "ai");
}));
$$("[data-ai-tool]").forEach(btn => btn.addEventListener("click", () => {
  state.selectedAiTool = btn.dataset.aiTool;
  $$("[data-ai-tool]").forEach(b => {
    b.classList.toggle("selected", b===btn);
    b.querySelector("b").textContent = b===btn ? "Selected" : "";
  });
}));

$("#resetEditBtn").addEventListener("click", () => {
  if (!state.image) return;
  state.modifiedUrl = state.originalUrl;
  $("#modifiedImage").src = state.originalUrl;
  resetTransforms();
  showToast("Edits reset.");
});

$("#applyStandardBtn").addEventListener("click", async () => {
  if (!state.image) return showToast("Choose an image first.");
  state.editType = "standard";
  if (!CONFIG.MOCK_MODE) {
    await fetch(CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.standardEdit, {
      method:"POST", headers:{"Content-Type":"application/json"},
      body:JSON.stringify({tool:"adjust",parameters:{brightness:state.brightness,contrast:state.contrast,saturation:state.saturation,rotation:state.rotation,flipH:state.flipH,flipV:state.flipV}})
    });
  }
  showToast("Standard edit applied.");
});

$("#applyAiBtn").addEventListener("click", async () => {
  if (!state.image) return showToast("Choose an image first.");
  state.editType = "ai";
  await simulateProcessing(state.selectedAiTool);
  if (!CONFIG.MOCK_MODE) {
    const res = await fetch(CONFIG.API_BASE_URL + CONFIG.ENDPOINTS.aiEdit, {
      method:"POST", headers:{"Content-Type":"application/json"},
      body:JSON.stringify({tool:state.selectedAiTool})
    });
    const data = await res.json();
    state.modifiedUrl = data.modified_url || data.url;
    $("#modifiedImage").src = state.modifiedUrl;
  } else {
    if (state.selectedAiTool === "color_fix") {
      state.brightness = 108; state.contrast = 112; state.saturation = 118;
    } else {
      state.contrast = 108; state.saturation = 106;
    }
    updateRangeLabels(); applyPreviewFilter();
  }
  showToast("AI enhancement completed.");
});

function simulateProcessing(tool) {
  return new Promise(resolve => {
    const modal=$("#processingModal"), bar=$("#processingBar"), msg=$("#processingMessage");
    $("#processingTitle").textContent = tool === "upscale" ? "AI upscaling image" : "Correcting image colors";
    modal.classList.remove("hidden");
    let value=0;
    const messages=["Preparing image...","Sending secure request...","Processing enhancement...","Finalizing result..."];
    const timer=setInterval(() => {
      value += 8 + Math.random()*12;
      if (value>100) value=100;
      bar.style.width=`${value}%`;
      msg.textContent=messages[Math.min(Math.floor(value/26),3)];
      if (value>=100) {
        clearInterval(timer);
        setTimeout(() => {modal.classList.add("hidden");bar.style.width="0";resolve();},400);
      }
    },180);
  });
}

$("#saveBtn").addEventListener("click", () => {
  if (!state.image) return showToast("Choose an image first.");
  const item = {
    id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()),
    name: state.fileName,
    originalUrl: state.originalUrl,
    modifiedUrl: state.modifiedUrl || state.originalUrl,
    editType: state.editType,
    date: new Date().toISOString()
  };
  state.gallery.unshift(item);
  localStorage.setItem("neuropix_gallery", JSON.stringify(state.gallery));
  updateDashboard(); renderGallery();
  showToast("Saved to the frontend demo gallery.");
});

$("#downloadBtn").addEventListener("click", () => {
  if (!state.modifiedUrl) return showToast("No processed image available.");
  const a=document.createElement("a");a.href=state.modifiedUrl;a.download=`processed-${state.fileName || "image"}`;a.click();
});

function renderGallery() {
  const query = ($("#gallerySearch")?.value || "").toLowerCase();
  const filter = $("#galleryFilter")?.value || "all";
  const items = state.gallery.filter(i => i.name.toLowerCase().includes(query) && (filter==="all" || i.editType===filter));
  const grid=$("#galleryGrid");
  if (!items.length) {
    grid.innerHTML = `<div class="panel empty-state" style="grid-column:1/-1"><div><span>▧</span><h3>No images found</h3><p>Process and save an image to see it here.</p></div></div>`;
    return;
  }
  grid.innerHTML=items.map(item => `
    <article class="gallery-card">
      <img src="${item.modifiedUrl}" alt="${escapeHtml(item.name)}">
      <div class="gallery-card-body">
        <h4>${escapeHtml(item.name)}</h4>
        <div class="gallery-meta"><span>${new Date(item.date).toLocaleDateString()}</span><span class="badge">${item.editType}</span></div>
        <div class="gallery-actions">
          <button data-open-id="${item.id}">Open</button>
          <button data-download-id="${item.id}">Download</button>
          <button class="delete" data-delete-id="${item.id}">Delete</button>
        </div>
      </div>
    </article>`).join("");

  $$("[data-open-id]").forEach(btn => btn.addEventListener("click", () => {
    const item=state.gallery.find(i=>i.id===btn.dataset.openId);
    state.originalUrl=item.originalUrl;state.modifiedUrl=item.modifiedUrl;state.fileName=item.name;state.editType=item.editType;
    $("#originalImage").src=item.originalUrl;$("#modifiedImage").src=item.modifiedUrl;
    $("#uploadZone").classList.add("hidden");$("#workspace").classList.remove("hidden");
    openAppPage("editor");
  }));
  $$("[data-download-id]").forEach(btn => btn.addEventListener("click", () => {
    const item=state.gallery.find(i=>i.id===btn.dataset.downloadId);
    const a=document.createElement("a");a.href=item.modifiedUrl;a.download=`processed-${item.name}`;a.click();
  }));
  $$("[data-delete-id]").forEach(btn => btn.addEventListener("click", () => {
    state.gallery=state.gallery.filter(i=>i.id!==btn.dataset.deleteId);
    localStorage.setItem("neuropix_gallery",JSON.stringify(state.gallery));
    updateDashboard();renderGallery();showToast("Image removed.");
  }));
}
$("#gallerySearch").addEventListener("input", renderGallery);
$("#galleryFilter").addEventListener("change", renderGallery);

$("#themeToggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
  $("#darkModeSetting").checked=document.body.classList.contains("dark");
  localStorage.setItem("neuropix_dark", document.body.classList.contains("dark"));
});
$("#darkModeSetting").addEventListener("change", e => {
  document.body.classList.toggle("dark", e.target.checked);
  localStorage.setItem("neuropix_dark", e.target.checked);
});
$("#compactSidebar").addEventListener("change", e => document.body.classList.toggle("compact", e.target.checked));
if (localStorage.getItem("neuropix_dark")==="true") {
  document.body.classList.add("dark");$("#darkModeSetting").checked=true;
}
function escapeHtml(str=""){return str.replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));}

route(state.user ? "app" : "landing");
