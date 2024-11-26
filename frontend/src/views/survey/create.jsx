import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

import apiInstance from "../../utils/axios";
import { surveycreate } from "../../utils/surveyCreate"; 

import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";

function CreateForm () {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [questions, setQuestions] = useState([{ text: "", question_type: "", options: [] }]);
  const [isPublished, setIsPublished] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const { error } = await surveycreate(title, description, isPublished, questions);
    if (error) {
      alert(error);
      setIsLoading(false);
    } else {
      navigate("/");
      alert("Survey form created!");
      setIsLoading(false);
    }
  };

  // Function to handle changes in individual questions
  const handleQuestionChange = (index, field, value) => {
    const newQuestions = [...questions];
    // newQuestions[index][field] to access the nested dictionary of key:field 
    newQuestions[index][field] = value;
    setQuestions(newQuestions);
  };

  // Function to add a new question to the survey
  const addQuestion = () => {
    setQuestions([...questions, { text: "", question_type: "", options: [] }]);
  };

  return (
    <>
      <BaseHeader />

      <section
        className="container d-flex flex-column vh-100"
        style={{ marginTop: "150px" }}
      >
        <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
          <div className="col-lg-5 col-md-8 py-8 py-xl-0">
            <div className="card shadow">
              <div className="card-body p-6">
                <div className="mb-4">
                  <h1 className="mb-1 fw-bold">Create Survey</h1>
                  <span>
                    <Link to="/">Back to Home</Link>
                  </span>
                </div>
                
                {/* Survey Form */}
                <form className="needs-validation" noValidate="" onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label htmlFor="title" className="form-label">
                      Survey Title
                    </label>
                    <input
                      type="text"
                      id="title"
                      className="form-control"
                      placeholder="Enter survey title"
                      required
                      value={title}
                      onChange={(e) => setTitle(e.target.value)}
                    />
                  </div>

                  <div className="mb-3">
                    <label htmlFor="description" className="form-label">
                      Description
                    </label>
                    <textarea
                      id="description"
                      className="form-control"
                      placeholder="Enter survey description"
                      required
                      value={description}
                      onChange={(e) => setDescription(e.target.value)}
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Questions</label>
                    {questions.map((question, index) => (
                      <div key={index} className="mb-2">
                        <input
                          type="text"
                          className="form-control mb-1"
                          placeholder="Enter question text"
                          value={question.text}
                          onChange={(e) => handleQuestionChange(index, "text", e.target.value)}
                        />
                        <select
                          className="form-control mb-1"
                          value={question.question_type}
                          onChange={(e) => handleQuestionChange(index, "question_type", e.target.value)}
                        >
                          <option value="">Select question type</option>
                          <option value="short_text">Short Text</option>
                          <option value="paragraph">Paragraph</option>
                          <option value="multiple_choice" type="radio">Multiple Choice</option>
                          <option value="checkbox" type="checkbox">Checkbox</option>
                          <option value="dropdown">Dropdown</option>
                        </select>
                        {/* You can add option inputs here if question type requires options */}
                      </div>
                    ))}
                    <button type="button" className="btn btn-link" onClick={addQuestion}>
                      Add Another Question
                    </button>
                  </div>

                  <div className="mb-3">
                    <label className="form-check-label" htmlFor="isPublished">
                      Publish Survey
                    </label>
                    <input
                      id="isPublished"
                      className="form-check-input ms-2"
                      checked={isPublished}
                      onChange={(e) => setIsPublished(e.target.checked)}
                    />
                  </div>

                  <div className="d-grid">
                    {isLoading ? (
                      <button disabled type="submit" className="btn btn-primary">
                        Processing <i className="fas fa-spinner fa-spin"></i>
                      </button>
                    ) : (
                      <button type="submit" className="btn btn-primary">
                        Create Survey <i className="fas fa-plus-circle"></i>
                      </button>
                    )}
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      <BaseFooter />
    </>
  );
}

export default CreateForm;