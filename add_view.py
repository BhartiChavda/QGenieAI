with open('QGenieAIapp/views.py', 'a', encoding='utf-8') as f:
    f.write('''

@login_required
def add_custom_question_view(request, file_id):
    """
    Allows a user to manually add a custom subjective question.
    The AI will automatically answer it based on the document text, and save it as a NormalQuestion.
    """
    if request.user.is_staff:
        file_obj = get_object_or_404(UploadedFile, id=file_id)
    else:
        file_obj = get_object_or_404(UploadedFile, id=file_id, user=request.user)

    if request.method == "POST":
        question_text = request.POST.get('question_text', '').strip()
        if not question_text:
            messages.error(request, "Question text cannot be empty.")
            return redirect('review_content', file_id=file_obj.id)
            
        try:
            # Extract text from file
            extracted_text = ""
            if file_obj.file_type == 'PDF':
                extracted_text = extract_text_from_pdf(file_obj.file.path)
            else:
                with open(file_obj.file.path, 'r', encoding='utf-8', errors='ignore') as f_read:
                    extracted_text = f_read.read()
                    
            # Use AI to answer the specific question based on the document
            ai_answer = chat_with_document(extracted_text, question_text)
            
            # Save it to the database
            NormalQuestion.objects.create(
                file=file_obj,
                question_text=question_text,
                answer=ai_answer
            )
            
            messages.success(request, "Custom question added and answered successfully by QGenie!")
        except Exception as e:
            messages.error(request, f"Failed to generate answer for your question: {str(e)}")
            
    return redirect('review_content', file_id=file_obj.id)
''')
