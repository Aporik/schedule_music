<script setup lang="ts">
import { computed, ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { api } from '@/api/client'
import type { Artist, YouTubeCoverVideo } from '@/api/types'
import PageHeader from '@/components/PageHeader.vue'

const selectedArtistId = ref<number | null>(null)
const query = ref('')
const artistsQuery = useQuery({ queryKey: ['artists'], queryFn: api.artists.list })
const coversQuery = useQuery({
  queryKey: computed(() => ['youtube-covers', selectedArtistId.value]),
  queryFn: () => api.youtubeCovers.list(selectedArtistId.value ?? undefined),
})

const artists = computed(() => artistsQuery.data.value ?? [])
const selectedArtist = computed(() => artists.value.find((artist) => artist.id === selectedArtistId.value) ?? null)
const covers = computed(() => {
  const needle = query.value.trim().toLocaleLowerCase()
  return (coversQuery.data.value ?? []).filter((cover) => !needle || [cover.video_title, cover.artist_name]
    .some((value) => value.toLocaleLowerCase().includes(needle)))
})

function chooseArtist(artist: Artist | null): void {
  selectedArtistId.value = artist?.id ?? null
}
function thumbnail(cover: YouTubeCoverVideo): string {
  return `https://i.ytimg.com/vi/${encodeURIComponent(cover.youtube_video_id)}/hqdefault.jpg`
}
function displayDate(value: string | null): string {
  if (!value) return '날짜 미확인'
  return new Intl.DateTimeFormat('ko-KR', { dateStyle: 'long' }).format(new Date(value))
}
</script>

<template>
  <div class="page">
    <PageHeader
      eyebrow="YOUTUBE ARCHIVE / COVERS"
      title="YouTube 커버곡"
      description="등록된 아티스트의 공식 채널에서 수집한 커버 영상을 한곳에서 확인합니다."
    />

    <section class="panel cover-browser">
      <div class="cover-browser__filters">
        <UButton class="button" :class="{ 'button--primary': !selectedArtist }" @click="chooseArtist(null)">전체 아티스트</UButton>
        <UButton v-for="artist in artists" :key="artist.id" class="button" :class="{ 'button--primary': artist.id === selectedArtistId }" @click="chooseArtist(artist)">
          {{ artist.display_name || artist.name }}
        </UButton>
      </div>
      <label class="cover-browser__search">
        <span class="sr-only">커버곡 검색</span>
        <UInput v-model="query" placeholder="곡명 또는 아티스트 검색" />
      </label>
    </section>

    <div v-if="coversQuery.isPending.value" class="skeleton-list"><i /><i /><i /></div>
    <div v-else-if="coversQuery.isError.value" class="empty-state">
      <strong>커버곡 목록을 불러오지 못했습니다.</strong>
      <p>API 연결 상태를 확인한 뒤 다시 시도해주세요.</p>
    </div>
    <div v-else-if="covers.length" class="cover-grid">
      <a v-for="cover in covers" :key="cover.id" class="cover-card" :href="cover.youtube_url" target="_blank" rel="noreferrer">
        <img :src="thumbnail(cover)" :alt="`${cover.video_title} 썸네일`" loading="lazy" />
        <div class="cover-card__body">
          <span>{{ cover.artist_name }}</span>
          <h2>{{ cover.video_title }}</h2>
          <p>{{ displayDate(cover.published_at) }}</p>
        </div>
      </a>
    </div>
    <div v-else class="empty-state">
      <strong>{{ selectedArtist ? `${selectedArtist.display_name || selectedArtist.name}의 커버곡이 아직 없습니다.` : '수집된 커버곡이 아직 없습니다.' }}</strong>
      <p>등록된 YouTube 채널을 수집하면 제목 또는 설명에 Cover·歌ってみた·カバー가 포함된 영상부터 표시됩니다.</p>
    </div>
  </div>
</template>

<style scoped>
.cover-browser { display: flex; gap: 1rem; align-items: flex-start; justify-content: space-between; margin-bottom: 1.5rem; }
.cover-browser__filters { display: flex; flex: 1; flex-wrap: wrap; gap: .5rem; }
.cover-browser__search { min-width: min(100%, 17rem); }
.cover-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 1rem; }
.cover-card { color: inherit; text-decoration: none; overflow: hidden; border: 1px solid var(--line); background: var(--panel); }
.cover-card img { width: 100%; aspect-ratio: 16 / 9; display: block; object-fit: cover; }
.cover-card__body { padding: .875rem; }
.cover-card__body span, .cover-card__body p { color: var(--muted); font-size: .82rem; }
.cover-card__body h2 { margin: .4rem 0; font-size: 1rem; line-height: 1.45; }
@media (max-width: 680px) { .cover-browser { flex-direction: column; } .cover-browser__search { width: 100%; } }
</style>
