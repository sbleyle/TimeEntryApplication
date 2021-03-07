USE [TimeEntryDB]
GO

/****** Object:  Table [dbo].[DimHourIncrements]    Script Date: 3/7/2021 2:58:38 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DimHourIncrements](
	[HourIncrements] [float] NOT NULL,
	[HourID] [nchar](10) NOT NULL
) ON [PRIMARY]
GO


