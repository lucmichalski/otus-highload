<template>
    <b-row>
        <b-col cols="9">
            <b-card style="margin-bottom: 5px;"
                    no-body
            >
                <b-card-body
                        class="text-muted"
                        style="background-color: #EFFCDE"
                >
                    {{ item['message'] }}
                </b-card-body>
                <template v-slot:footer>
                    <div class="text-left">
                        <b-avatar
                                button
                                variant="secondary"
                                :size="20"
                                class="align-center"
                                @click="onProfileClick($event, item['user_id'])"
                        ></b-avatar>
                        <span class="small text-muted">{{ item['user_name'] }}, {{ item['date_create'] }}</span>
                    </div>
                </template>
            </b-card>
        </b-col>
        <b-col cols="3"></b-col>
    </b-row>
</template>

<script>
    export default {
        props: {
            item: Object | Array,
            followerUrl: String,
        },
        methods: {
            onProfileClick: function (e, id) {
                window.open(this.populateUrl(this.followerUrl, {id: id}), '_blank');
            }
        }
    }
</script>

<style scoped>

</style>