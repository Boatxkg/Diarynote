<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">My Notes</h1>
    <div class="m-3 flex">
      <input type="text" v-model="search" placeholder="ค้นหาอะไรสักอย่าง" class="p-3">
      <button type="button" @click="searchNotes" class="px-2 pe-2 pt-0 px-0 bg-blue-500 text-white rounded cursor-pointer">ค้นหา</button>
    </div>
    <div class="flex gap-2 mb-4">
      <input v-model="title" placeholder="Title" class="border p-2 w-1/3 rounded" />
      <input v-model="content" placeholder="Content" class="border p-2 flex-1 rounded" />
      <button @click="createNote" class="bg-green-500 text-white p-2 rounded cursor-pointer" type="button">Add</button>
    </div>

    <NoteCard
        v-for="note in notes"
        :key="note.id"
        :note="note"
        @delete="handleDelete"
        @update="handleUpdate"
    />
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import NoteCard from '../components/NoteCard.vue'

const title = ref('')
const content = ref('')
const search = ref('')
const notes = ref([])

const handleDelete = async (id) => {
  try {
    await deleteNote(id)
    notes.value = notes.value.filter(note => note.id !== id)
  } catch (e) {
    console.error('Delete failed:', e)
    alert('ลบไม่สำเร็จ')
  }
}

const handleUpdate = (updatedNote) => {
  const index = notes.value.findIndex(note => note.id === updatedNote.id)
  if (index !== -1) {
    notes.value[index] = updatedNote
  }
}

const fetchNotes = async () => {
  const token = localStorage.getItem('token')
  const res = await axios.get('http://localhost:5000/api/notes', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  notes.value = res.data
}

const createNote = async () => {
  const token = localStorage.getItem('token')
  try {
    await axios.post('http://localhost:5000/api/notes', {
      title: title.value,
      content: content.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    title.value = ''
    content.value = ''
    fetchNotes()
  } catch (e) {
    console.error('Create note failed:', e)
  }
}

const deleteNote = async (id) => {
  const token = localStorage.getItem('token')
  await axios.delete(`http://localhost:5000/api/notes/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  fetchNotes()
}

const editNote = async (id) => {
  const token = localStorage.getItem('token')
  try {
    await axios.put(`http://localhost:5000/api/notes/${id}`, {
      title: title.value,
      content: content.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    title.value = ''
    content.value = ''
    fetchNotes()
  } catch (e) {
    console.error('Edit note failed:', e)  // แก้ข้อความ error ให้ตรงกับฟังก์ชัน
  }
}
const searchNotes = async () => {
  const token = localStorage.getItem('token')
  const baseUrl = 'http://localhost:5000/api/notes'

  // ถ้าไม่มีคำค้น ให้เรียก /notes ธรรมดา
  const url = search.value.trim()
    ? `${baseUrl}/${encodeURIComponent(search.value.trim())}`
    : baseUrl

  try {
    const res = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    notes.value = res.data
  } catch (e) {
    console.error('Search failed:', e)
  }
}


onMounted(fetchNotes)
</script>

