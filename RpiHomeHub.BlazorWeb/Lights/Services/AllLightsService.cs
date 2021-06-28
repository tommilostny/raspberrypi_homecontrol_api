﻿using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Lights.Models;
using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public class AllLightsService : LightServiceBase, ILightService
    {
        public AllLightsService(HttpClient httpClient) : base(httpClient)
        {
        }

        public Task<ILightModel> GetStatus() => throw new NotImplementedException();

        public async Task<IEnumerable<ILightModel>> GetAllStatus()
        {
            var lampTask = _httpClient.GetAsync("lamp");
            var yeelightTask = _httpClient.GetAsync("yeelight");
            var stripTask = _httpClient.GetAsync("ledstrip");

            var statuses = new List<ILightModel>();
            await Task.WhenAll(lampTask, yeelightTask, stripTask);

            statuses.Add(JsonConvert.DeserializeObject<LampModel>(await lampTask.Result.Content.ReadAsStringAsync()));
            statuses.Add(JsonConvert.DeserializeObject<YeelightModel>(await yeelightTask.Result.Content.ReadAsStringAsync()));
            statuses.Add(JsonConvert.DeserializeObject<LED_StripModel>(await stripTask.Result.Content.ReadAsStringAsync()));
            return statuses;
        }

        public async Task<ILightModel> Toggle()
        {
            await _httpClient.GetAsync("lights/toggle");
            return await GetStatus();
        }

        public async Task<ILightModel> TurnOff()
        {
            await _httpClient.GetAsync("lights/off");
            return await GetStatus();
        }

        public async Task<ILightModel> TurnOn()
        {
            await _httpClient.GetAsync("lights/on");
            return await GetStatus();
        }

        public async Task<ILightModel> SetColor(int red, int green, int blue)
        {
            await _httpClient.GetAsync($"lights/{red}/{green}/{blue}");
            return await GetStatus();
        }

        public async Task<ILightModel> SetBrightness(int brightness)
        {
            await _httpClient.GetAsync($"lights/{brightness}");
            return await GetStatus();
        }
    }
}
