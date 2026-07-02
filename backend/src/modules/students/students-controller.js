const asyncHandler = require("express-async-handler");
const { getAllStudents, addNewStudent, getStudentDetail, setStudentStatus, updateStudent } = require("./students-service");

const handleGetAllStudents = asyncHandler(async (req, res) => {
    const students = await getAllStudents(req.query);
    res.json({ students });
});

const handleAddStudent = asyncHandler(async (req, res) => {
    const result = await addNewStudent(req.body);
    res.json(result);
});

const handleUpdateStudent = asyncHandler(async (req, res) => {
    const payload = { ...req.body, userId: req.params.id };
    const result = await updateStudent(payload);
    res.json(result);
});

const handleGetStudentDetail = asyncHandler(async (req, res) => {
    const student = await getStudentDetail(req.params.id);
    res.json(student);
});

const handleStudentStatus = asyncHandler(async (req, res) => {
    const payload = {
        userId: req.params.id,
        reviewerId: req.user.id,
        status: req.body.status
    };
    const result = await setStudentStatus(payload);
    res.json(result);
});

module.exports = {
    handleGetAllStudents,
    handleGetStudentDetail,
    handleAddStudent,
    handleStudentStatus,
    handleUpdateStudent,
};
