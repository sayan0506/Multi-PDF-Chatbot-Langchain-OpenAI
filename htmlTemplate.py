# in the css template where the bot_template, user-template elements are arranged are mentioned
css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

# defining the templates for the bot
# creates a single class, which returns the bot message
# the following template will communicate to streamlit in order to retrive llm respones and show it to the user using following template
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
# in the above code two classes are there, avatar class shows an image as avatar
# message class shows the message

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
# same here avatar creates an avatar for user
# message class returns the message

#https://media.istockphoto.com/id/1467878602/photo/humanoid-robots-revolutionizing-mundane-tasks.jpg?s=612x612&w=is&k=20&c=KoiOJk_QjwYQzyUQKhi7i8hf0QScjf1P_LpUnrwhDho=