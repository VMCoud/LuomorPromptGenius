function gen_class_card_html(class_id, class_name, example_desc) {
  html = `
    <div class="mdui-col class-card-col">
        <div class="mdui-card class-card mdui-hoverable" id="class-card-${class_id}" classid="${class_id}">
            <div class="mdui-card-primary class-card-primary">
                <div class="mdui-card-primary-title">${class_name}</div>
            </div>
            <div class="mdui-card-content">${example_desc}</div>
        </div>
    </div>
    `
  return html
}



function generate_prompt_card_html(index, item) {
  chat_list = item['chat_list']
  class_list = item['class_list']
  author = item['author']
  author_link = item['author_link']
  model = item['model']
  function_desc = item['function_desc']
  prompt_text = chat_list[0]
  class_name = class_list[0]
  icon_name = item['icon_name']
  icon_style = item['icon_style']
  example_desc = prompt_text

  icon_html = `<span class="${icon_style}">${icon_name}</span>  
          `

  // <div class="mdui-col-xs-6 mdui-col-sm-6 mdui-col-md-4 mdui-col-lg-3 mdui-col-xl-3 mdui-m-t-2">
  // <span className="mdui-icon material-icons mdui-text-color-blue">lightbulb_outline</span>
  html = `
    <div class="mdui-col-xs-12 mdui-col-sm-12 mdui-col-md-12 mdui-col-lg-12 mdui-col-xl-12 mdui-m-t-12 mdui-m-b-2">
      <div class="mdui-card mdui-shadow-4 prompt-card">
        <div class="mdui-card-primary mdui-color-grey-50 prompt-card-header">
          
          
          ${icon_html}
          <span class="mdui-chip mdui-color-theme-200">
            <div class="mdui-chip-title">${class_name}</div>
          </span>

          <span class="mdui-chip mdui-color-theme-400">
              <div class="mdui-chip-title ">${function_desc}</div>
          </span>

          <span class="mdui-chip mdui-color-grey-50">
            <a href="${author_link}"> 
            <div class="mdui-chip-title mdui-text-color-theme-text">${author}</div>
            </a>
          </span>
          
          <button style="z-index:100" class="mdui-btn mdui-float-right mdui-color-light-blue-50" id="copy-message-${index}">copy</button>

        </div>

        <div class="mdui-card-primary mdui-p-a-0">    
          <div class="mdui-card-content mdui-text-color-theme-text" id="class-card-${index}" class_id="${index}" > ${prompt_text} </div>
        </div>

        </div>
      </div>
    </div>
  `
  return html;
}


// mdui-p-a-0: bottom and up and padding



